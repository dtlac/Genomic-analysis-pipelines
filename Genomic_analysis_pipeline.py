#!/usr/bin/env python3
"""
Genomic Variant Calling Pipeline
=================================
End-to-end pipeline: raw paired-end FASTQ → filtered SNP/INDEL tables.
Works with any reference genome and any organism ploidy.

Conda environment layout
-------------------------
This pipeline is designed for the common setup where:

  • GATK is installed in the conda **base** environment.
  • All other tools (Trimmomatic, BWA, Picard, samtools, bcftools,
    bgzip, tabix) live in a separate named conda environment.

Pass that named environment with --main-env.  GATK commands are always
run in base (no wrapping needed — base is the default shell environment).

If everything shares a single environment, omit --main-env and GATK will
also be found on PATH without any extra flag.

                ┌─────────────────────────────────────┐
                │ conda base                          │
                │   gatk                              │
                └─────────────────────────────────────┘
                ┌─────────────────────────────────────┐
                │ --main-env  (e.g. genome-analysis)  │
                │   trimmomatic  bwa  picard  samtools │
                │   bcftools  bgzip  tabix             │
                └─────────────────────────────────────┘

Every non-GATK command is prefixed with:
    conda run -n <main-env> --no-capture-output <tool> ...
Every GATK command calls gatk directly (runs in base, the active shell).

Ancestor VCF modes
------------------
Mode A — pre-existing VCFs:
    Pass --ancestor-vcf-dir and one or more --ancestor-vcf filenames.
    The pipeline uses those VCFs directly in step 9 filtering.

Mode B — raw FASTQ ancestors:
    Pass --ancestor-fastq-dir pointing to a folder of paired-end FASTQ files.
    Steps 1-8 are run on those files first (in <project-dir>/Ancestor/),
    then the resulting VCFs are used for filtering.
    Both modes fully support the base-vs-main-env layout described above.

Usage examples
--------------
# GATK in base, other tools in genome-analysis env, Mode A ancestors
python genomic_variant_pipeline.py \\
    --project-dir      /data/project \\
    --ref-dir          /refs/genome_dir \\
    --ref-name         genome_v1.fa \\
    --main-env         genome-analysis \\
    --ancestor-vcf-dir /refs/ancestor_vcfs \\
    --ancestor-vcf     PM_t0.vcf.gz \\
    --ancestor-vcf     PA_t0.vcf.gz \\
    --ploidy 4 --threads 20

# Same layout, Mode B — pipeline processes ancestor FASTQs first
python genomic_variant_pipeline.py \\
    --project-dir        /data/project \\
    --ref-dir            /refs/genome_dir \\
    --ref-name           genome_v1.fa \\
    --main-env           genome-analysis \\
    --ancestor-fastq-dir /data/ancestor_reads \\
    --ploidy 4 --threads 20

# All tools in one environment (no --main-env needed)
python genomic_variant_pipeline.py \\
    --project-dir      /data/project \\
    --ref-dir          /refs/genome_dir \\
    --ref-name         genome_v1.fa \\
    --ancestor-vcf-dir /refs/ancestor_vcfs \\
    --ancestor-vcf     ancestor.vcf.gz \\
    --ploidy 2 --threads 8

Requirements:
    trimmomatic, bwa, picard, samtools, bcftools, bgzip, tabix  (main env)
    gatk                                                         (base env)
"""

import sys
import subprocess
import argparse
import logging
from contextlib import contextmanager
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────

def setup_logging(log_file: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(str(log_file), mode="a"),
        ],
    )

log = logging.getLogger("pipeline")


# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

class Config:
    """
    Central configuration object.
    Every path, environment name, and tunable parameter lives here so nothing
    is hard-coded elsewhere in the script.

    Environment model
    -----------------
    main_env : str | None
        The conda environment that holds all non-GATK tools
        (Trimmomatic, BWA, Picard, samtools, bcftools, bgzip, tabix).
        Every command for these tools is prefixed with:
            conda run -n <main_env> --no-capture-output
        Set to None when all tools (including GATK) share the active shell
        environment and no wrapping is needed.

    GATK runs in the conda base environment — the default shell — so it
    is always called directly without any conda run prefix.  This works
    correctly whether the user activated base or runs the script from a
    launcher, because base is always present and on PATH before any other
    environment is activated.
    """

    def __init__(self, args):
        # ── Reference genome ─────────────────────────────────────────────────
        self.ref_dir  = Path(args.ref_dir)
        self.ref_name = args.ref_name               # e.g. genome_v1.fa
        self.ref      = self.ref_dir / self.ref_name

        # ── Sample project ───────────────────────────────────────────────────
        self.project_dir      = Path(args.project_dir)
        self.raw_dir          = self.project_dir / "Raw"
        self.trimmed_paired   = self.project_dir / "Trimmomatic" / "Paired"
        self.trimmed_unpaired = self.project_dir / "Trimmomatic" / "Unpaired"
        self.aligned_dir      = self.project_dir / "1.Aligned"
        self.sorted_dir       = self.project_dir / "2.Sorted"
        self.marked_dir       = self.project_dir / "3.Marked_duplicates"
        self.fixed_rg_dir     = self.project_dir / "4.Fixed_read_group"
        self.vcf_dir          = self.project_dir / "5.Variants_call"
        self.variants_dir     = self.project_dir / "6.Hard_filtered_variants"

        # ── Conda environment ────────────────────────────────────────────────
        # main_env: conda env for Trimmomatic, BWA, Picard, samtools,
        #           bcftools, bgzip, tabix.
        #           None = tools are on PATH in the current shell (no wrapping).
        # GATK lives in conda base and is always called directly — no env arg.
        self.main_env: str | None = args.main_env or None

        # ── Ancestor mode ────────────────────────────────────────────────────
        if args.ancestor_fastq_dir:
            self.ancestor_mode      = "b"
            self.ancestor_fastq_dir = Path(args.ancestor_fastq_dir)
            self.ancestor_project   = self.project_dir / "Ancestor"
            self.ancestor_vcf_dir   = self.ancestor_project / "5.Variants_call"
            self.ancestor_vcfs: list[Path] = []
        else:
            self.ancestor_mode      = "a"
            self.ancestor_fastq_dir = None
            self.ancestor_project   = None
            anc_dir = Path(args.ancestor_vcf_dir)
            self.ancestor_vcf_dir   = anc_dir
            self.ancestor_vcfs      = [anc_dir / n for n in (args.ancestor_vcf or [])]

        # ── Run options ──────────────────────────────────────────────────────
        self.ploidy     = args.ploidy
        self.threads    = args.threads
        self.skip_index = args.skip_index
        self.start_step = args.start_step

        # ── Trimmomatic knobs ────────────────────────────────────────────────
        self.trim_leading  = args.trim_leading
        self.trim_trailing = args.trim_trailing
        self.trim_window   = args.trim_window
        self.trim_quality  = args.trim_quality
        self.trim_minlen   = args.trim_minlen
        self.trim_headcrop = args.trim_headcrop
        self.trim_crop     = args.trim_crop

    def validate(self) -> None:
        """Fail fast with clear messages before any tool is called."""
        errors: list[str] = []

        if not self.ref_dir.is_dir():
            errors.append(f"--ref-dir not found: {self.ref_dir}")
        elif not self.ref.exists():
            errors.append(f"Reference FASTA not found: {self.ref}")

        if self.ancestor_mode == "a":
            if not self.ancestor_vcf_dir.is_dir():
                errors.append(f"--ancestor-vcf-dir not found: {self.ancestor_vcf_dir}")
            for vcf in self.ancestor_vcfs:
                if not vcf.exists():
                    errors.append(f"Ancestor VCF not found: {vcf}")
            if not self.ancestor_vcfs:
                errors.append("Mode A requires at least one --ancestor-vcf filename.")
        else:
            if not self.ancestor_fastq_dir.is_dir():
                errors.append(f"--ancestor-fastq-dir not found: {self.ancestor_fastq_dir}")

        # Verify --main-env exists (if specified)
        if self.main_env and not _conda_env_exists(self.main_env):
            errors.append(
                f"--main-env conda environment not found: '{self.main_env}'\n"
                f"  Run 'conda env list' to see available environments."
            )

        # Verify GATK is reachable in base
        if not _tool_in_base("gatk"):
            errors.append(
                "gatk not found in the conda base environment.\n"
                "  Install GATK in base or adjust your PATH."
            )

        if errors:
            for e in errors:
                log.error(e)
            sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Conda / tool availability helpers
# ─────────────────────────────────────────────────────────────────────────────

def _conda_env_exists(env_name: str) -> bool:
    """Return True if a conda environment with this name exists."""
    r = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        parts = line.split()
        # Lines look like: "myenv   /path/to/envs/myenv" or "base * /path"
        if parts and parts[0] == env_name:
            return True
    return False


def _tool_in_base(tool: str) -> bool:
    """
    Return True if `tool` is on the PATH in the base conda environment.

    Uses `conda run -n base which <tool>` so we check base specifically,
    not the currently active env.
    """
    r = subprocess.run(
        ["conda", "run", "-n", "base", "--no-capture-output", "which", tool],
        capture_output=True, text=True,
    )
    return r.returncode == 0



# ─────────────────────────────────────────────────────────────────────────────
# Context manager for logging environment transitions
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def conda_env_block(env_label: str, tool_label: str):
    """
    Logs a clear enter/leave boundary around a block of tool calls that
    share the same conda environment.  Purely for log readability —
    actual environment routing is handled per-command by run_main / run_gatk.

    Usage:
        with conda_env_block("base", "GATK HaplotypeCaller"):
            run_gatk([...], cfg=cfg)
    """
    log.info(f"┌─ [{env_label}]  {tool_label}")
    try:
        yield
    finally:
        log.info(f"└─ [{env_label}]  {tool_label}  done")


# ─────────────────────────────────────────────────────────────────────────────
# Command runners
# ─────────────────────────────────────────────────────────────────────────────

def _exec(cmd: list, step: str) -> None:
    """Execute a command list, streaming output to the log; exit on failure."""
    log.info(f"[{step}] {' '.join(str(c) for c in cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout:
        log.info(r.stdout.strip())
    if r.stderr:
        log.warning(r.stderr.strip())
    if r.returncode != 0:
        log.error(f"[{step}] command failed (exit {r.returncode})")
        sys.exit(r.returncode)


def run_main(cmd: list, step: str, cfg: Config) -> None:
    """
    Run a non-GATK tool command (Trimmomatic, BWA, Picard, samtools,
    bcftools, bgzip, tabix).

    If --main-env was given, the command is wrapped with:
        conda run -n <main_env> --no-capture-output <cmd>
    Otherwise it runs directly in the current shell (tools must be on PATH).
    """
    if cfg.main_env:
        cmd = ["conda", "run", "-n", cfg.main_env,
               "--no-capture-output"] + list(cmd)
    _exec(cmd, step)


def run_gatk(gatk_args: list, step: str, cfg: Config) -> None:
    """
    Run a GATK command in the conda base environment.

    GATK is expected in base, so it is called via:
        conda run -n base --no-capture-output gatk <args>

    This works regardless of which environment the script itself was started
    from (main-env, another env, or base), because conda base is always
    present.  The explicit `-n base` also makes the routing transparent in
    the log output.
    """
    cmd = ["conda", "run", "-n", "base",
           "--no-capture-output", "gatk"] + list(gatk_args)
    _exec(cmd, step)


# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def mkdirs(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def compress_and_index(vcf: Path, step: str, cfg: Config) -> Path:
    """
    bgzip + tabix a VCF if not already done.
    bgzip and tabix live in the main env.
    Always returns the .vcf.gz path.
    """
    if vcf.suffix == ".vcf":
        gz = vcf.with_suffix(".vcf.gz")
        if not gz.exists():
            run_main(["bgzip", str(vcf)], step=step, cfg=cfg)
    else:
        gz = vcf
    if not Path(str(gz) + ".tbi").exists():
        run_main(["tabix", str(gz)], step=step, cfg=cfg)
    return gz


# ─────────────────────────────────────────────────────────────────────────────
# Core sample-processing steps  (steps 1-8)
# Functions accept explicit src/dst paths so they are reusable for both the
# main sample set and the ancestor FASTQ set (mode B).
# ─────────────────────────────────────────────────────────────────────────────

def run_trimmomatic(raw_dir: Path, paired_dir: Path,
                    unpaired_dir: Path, cfg: Config) -> None:
    """
    Step 1 — Quality trimming with Trimmomatic.   [main env]

    Trims adapters and low-quality bases from paired-end reads.
        LEADING/TRAILING  : drop end bases below the given quality
        SLIDINGWINDOW     : cut when a window average drops below threshold
        MINLEN            : discard reads shorter than this after trimming
        HEADCROP          : remove fixed N bases from the 5' end
        CROP              : hard-clip reads to this maximum length
    """
    mkdirs(paired_dir, unpaired_dir)
    r1_files = sorted(raw_dir.glob("*_R1_001.fastq.gz"))
    if not r1_files:
        log.warning(f"  No R1 FASTQ files found in {raw_dir} — skipping trimming.")
        return
    for r1 in r1_files:
        stem = r1.name[:-len("_R1_001.fastq.gz")]
        r2   = raw_dir / f"{stem}_R2_001.fastq.gz"
        if not r2.exists():
            log.warning(f"  R2 not found for {r1.name} — skipping pair.")
            continue
        run_main([
            "trimmomatic", "PE", "-phred33",
            str(r1), str(r2),
            str(paired_dir   / f"{stem}_R1_paired.fastq"),
            str(unpaired_dir / f"{stem}_R1_unpaired.fastq"),
            str(paired_dir   / f"{stem}_R2_paired.fastq"),
            str(unpaired_dir / f"{stem}_R2_unpaired.fastq"),
            f"LEADING:{cfg.trim_leading}",
            f"TRAILING:{cfg.trim_trailing}",
            f"SLIDINGWINDOW:{cfg.trim_window}:{cfg.trim_quality}",
            f"MINLEN:{cfg.trim_minlen}",
            f"HEADCROP:{cfg.trim_headcrop}",
            f"CROP:{cfg.trim_crop}",
        ], step="trimmomatic", cfg=cfg)


def run_index_reference(cfg: Config) -> None:
    """
    Step 2 — Reference genome indexing.   [main env + base env]

    Three commands are run in sequence; all are idempotent (output files
    are checked before running so reruns are safe):

    2a. BWA index   [main env]
        Builds the BWT/SA index BWA MEM needs for rapid read alignment.
        Uses the 'bwtsw' algorithm, suited for large genomes (>10 MB).
        Produces:  <ref>.amb  .ann  .bwt  .pac  .sa

    2b. samtools faidx   [main env]
        Creates a FASTA index (.fai) that allows fast random access to
        any region of the reference.  Required by samtools faidx calls
        in the repeat-filter step and by GATK tools.
        Produces:  <ref>.fai

    2c. GATK CreateSequenceDictionary   [base env]
        Builds a sequence dictionary (.dict) listing contig names, lengths,
        and MD5 checksums.  GATK HaplotypeCaller and VariantFiltration
        refuse to run without this file.  Called via gatk in the base
        conda environment, exactly like all other GATK commands.
        Produces:  <ref_stem>.dict

    Skip all three on reruns with --skip-index.
    """
    ref = cfg.ref
    fai  = Path(str(ref) + ".fai")
    dict_file = ref.with_suffix(".dict")

    # ── 2a: BWA index   [main env] ───────────────────────────────────────────
    bwt = Path(str(ref) + ".bwt")
    if bwt.exists():
        log.info(f"  BWA index already exists ({bwt.name}) — skipping bwa index.")
    else:
        with conda_env_block(cfg.main_env or "current shell", "bwa index"):
            run_main(
                ["bwa", "index", "-a", "bwtsw", str(ref)],
                step="2a-bwa-index", cfg=cfg,
            )

    # ── 2b: samtools faidx   [main env] ──────────────────────────────────────
    if fai.exists():
        log.info(f"  FASTA index already exists ({fai.name}) — skipping samtools faidx.")
    else:
        with conda_env_block(cfg.main_env or "current shell", "samtools faidx"):
            run_main(
                ["samtools", "faidx", str(ref)],
                step="2b-samtools-faidx", cfg=cfg,
            )

    # ── 2c: GATK CreateSequenceDictionary   [base env] ──────────────────────
    if dict_file.exists():
        log.info(f"  Sequence dictionary already exists ({dict_file.name}) — skipping.")
    else:
        with conda_env_block("base", "GATK CreateSequenceDictionary"):
            run_gatk([
                "CreateSequenceDictionary",
                "-R", str(ref),
                "-O", str(dict_file),
            ], step="2c-gatk-dict", cfg=cfg)


def run_align_and_sort(trimmed_paired: Path, sorted_dir: Path,
                       aligned_dir: Path, cfg: Config) -> None:
    """
    Step 3 — BWA MEM alignment → Picard SortSam.   [main env]

    Aligns trimmed reads to the reference and coordinate-sorts to BAM.
    Intermediate SAM files are deleted after sorting to save disk space.
    """
    mkdirs(aligned_dir, sorted_dir)
    r1_files = sorted(trimmed_paired.glob("*_R1_paired.fastq"))
    if not r1_files:
        log.warning(f"  No trimmed R1 files in {trimmed_paired} — skipping alignment.")
        return
    for r1 in r1_files:
        stem = r1.name.replace("_R1_paired.fastq", "")
        r2   = trimmed_paired / f"{stem}_R2_paired.fastq"
        sam  = aligned_dir   / f"{stem}.sam"
        bam  = sorted_dir    / f"{stem}_sorted.bam"
        run_main(
            ["bwa", "mem", "-t", str(cfg.threads),
             str(cfg.ref), str(r1), str(r2), "-o", str(sam)],
            step="bwa-mem", cfg=cfg,
        )
        run_main(
            ["picard", "SortSam",
             f"INPUT={sam}", f"OUTPUT={bam}",
             "SORT_ORDER=coordinate"],
            step="sortsam", cfg=cfg,
        )
        sam.unlink(missing_ok=True)


def run_index_bam(sorted_dir: Path, cfg: Config) -> None:
    """
    Step 4 — Picard BuildBamIndex.   [main env]

    Generates a .bai index alongside each sorted BAM for random access.
    """
    for bam in sorted(sorted_dir.glob("*_sorted.bam")):
        run_main(
            ["picard", "BuildBamIndex", f"INPUT={bam}", f"OUTPUT={bam}"],
            step="index-bam", cfg=cfg,
        )


def run_mark_duplicates(sorted_dir: Path, marked_dir: Path,
                        cfg: Config) -> None:
    """
    Step 5 — Picard MarkDuplicates.   [main env]

    Flags PCR/optical duplicates; reads are kept, not removed.
    GATK HaplotypeCaller ignores flagged duplicates automatically.
    Writes a per-sample metrics file with the duplication rate.
    """
    mkdirs(marked_dir)
    for bam in sorted(sorted_dir.glob("*_sorted.bam")):
        stem = bam.name[:-len("_sorted.bam")]
        run_main([
            "picard", "MarkDuplicates",
            "VALIDATION_STRINGENCY=LENIENT",
            f"INPUT={bam}",
            f"OUTPUT={marked_dir / f'{stem}_marked.bam'}",
            f"METRICS_FILE={marked_dir / f'{stem}_metrics.txt'}",
        ], step="mark-dups", cfg=cfg)


def run_fix_read_groups(marked_dir: Path, fixed_rg_dir: Path,
                        cfg: Config) -> None:
    """
    Step 6 — Picard AddOrReplaceReadGroups.   [main env]

    Writes @RG tags required by GATK (RGID, RGLB, RGPL, RGPU, RGSM).
    The sample name (RGSM) is derived from the filename stem.
    """
    mkdirs(fixed_rg_dir)
    for bam in sorted(marked_dir.glob("*_marked.bam")):
        stem = bam.name[:-len("_marked.bam")]
        run_main([
            "picard", "AddOrReplaceReadGroups",
            "VALIDATION_STRINGENCY=LENIENT",
            f"I={bam}",
            f"O={fixed_rg_dir / f'{stem}_fixed.bam'}",
            "RGID=4", "RGLB=lib1", "RGPL=illumina", "RGPU=unit1",
            f"RGSM={stem}",
        ], step="fix-rg", cfg=cfg)


def run_index_fixed_bams(fixed_rg_dir: Path, cfg: Config) -> None:
    """
    Step 7 — samtools index.   [main env]

    Re-indexes the read-group-corrected BAMs.  A fresh .bai is required
    because the BAM header changed in step 6.
    """
    for bam in sorted(fixed_rg_dir.glob("*_fixed.bam")):
        run_main(
            ["samtools", "index", str(bam)],
            step="index-fixed", cfg=cfg,
        )


def run_call_variants(fixed_rg_dir: Path, vcf_dir: Path,
                      cfg: Config) -> None:
    """
    Step 8 — GATK HaplotypeCaller.   [base env]

    Calls SNPs and INDELs via local re-assembly.  Key settings:
        --ploidy N             organism ploidy (2 = diploid, 4 = tetraploid…)
        -A FisherStrand        strand-bias FS annotation
        -A StrandBiasBySample  per-sample SB tag
        -A StrandOddsRatio     SOR strand-bias metric
        -A AlleleFraction      AF annotation for downstream filtering

    GATK runs in conda base; bgzip/tabix run in main env.
    """
    mkdirs(vcf_dir)
    with conda_env_block("base", "HaplotypeCaller"):
        for bam in sorted(fixed_rg_dir.glob("*_fixed.bam")):
            stem = bam.name[:-len("_fixed.bam")]
            vcf  = vcf_dir / f"{stem}.vcf"
            run_gatk([
                "HaplotypeCaller",
                "--native-pair-hmm-threads", str(cfg.threads),
                "-I", str(bam),
                "-O", str(vcf),
                "-R", str(cfg.ref),
                "-A", "FisherStrand",
                "-A", "StrandBiasBySample",
                "-A", "StrandOddsRatio",
                "-A", "AlleleFraction",
                "--ploidy", str(cfg.ploidy),
            ], step="haplotypecaller", cfg=cfg)

    # bgzip/tabix live in main env
    for vcf in sorted(vcf_dir.glob("*.vcf")):
        compress_and_index(vcf, step="compress-vcf", cfg=cfg)


# ─────────────────────────────────────────────────────────────────────────────
# Ancestor pipeline  (mode B)
# Runs steps 1-8 on ancestor FASTQs; fully respects base/main-env split.
# ─────────────────────────────────────────────────────────────────────────────

def process_ancestor_fastqs(cfg: Config) -> list[Path]:
    """
    Mode B — build ancestor VCFs from raw FASTQ files.

    Runs the full pre-processing + variant-calling pipeline (steps 1-8) in
    <project_dir>/Ancestor/ using the same reference, ploidy, thread count,
    and conda environment layout as the main sample run:
        steps 1-7  →  main env  (Trimmomatic, BWA, Picard, samtools)
        step  8    →  base env  (GATK HaplotypeCaller)

    Returns paths to the produced *.vcf.gz files used by step 9 filtering.
    """
    log.info("═" * 60)
    log.info("ANCESTOR MODE B — processing ancestor FASTQ files")
    log.info(f"  Source FASTQs : {cfg.ancestor_fastq_dir}")
    log.info(f"  Output dir    : {cfg.ancestor_project}")
    log.info(f"  Main env      : {cfg.main_env or '(current shell)'}")
    log.info(f"  GATK env      : base")
    log.info("═" * 60)

    anc          = cfg.ancestor_project
    paired_dir   = anc / "Trimmomatic" / "Paired"
    unpaired_dir = anc / "Trimmomatic" / "Unpaired"
    aligned_dir  = anc / "1.Aligned"
    sorted_dir   = anc / "2.Sorted"
    marked_dir   = anc / "3.Marked_duplicates"
    fixed_rg_dir = anc / "4.Fixed_read_group"
    vcf_dir      = anc / "5.Variants_call"
    mkdirs(anc)

    log.info("── Ancestor [main env]: quality trimming")
    run_trimmomatic(cfg.ancestor_fastq_dir, paired_dir, unpaired_dir, cfg)

    if not cfg.skip_index:
        log.info("── Ancestor [main env]: index reference (shared with main run)")
        run_index_reference(cfg)

    log.info("── Ancestor [main env]: align + sort")
    run_align_and_sort(paired_dir, sorted_dir, aligned_dir, cfg)

    log.info("── Ancestor [main env]: index sorted BAMs")
    run_index_bam(sorted_dir, cfg)

    log.info("── Ancestor [main env]: mark duplicates")
    run_mark_duplicates(sorted_dir, marked_dir, cfg)

    log.info("── Ancestor [main env]: fix read groups")
    run_fix_read_groups(marked_dir, fixed_rg_dir, cfg)

    log.info("── Ancestor [main env]: index fixed BAMs")
    run_index_fixed_bams(fixed_rg_dir, cfg)

    log.info("── Ancestor [base env]: call variants (GATK)")
    run_call_variants(fixed_rg_dir, vcf_dir, cfg)

    ancestor_vcfs = sorted(vcf_dir.glob("*.vcf.gz"))
    if not ancestor_vcfs:
        log.error("Ancestor processing produced no VCF files — aborting.")
        sys.exit(1)

    log.info(f"Ancestor VCFs produced ({len(ancestor_vcfs)}):")
    for v in ancestor_vcfs:
        log.info(f"  {v}")
    log.info("═" * 60)
    return ancestor_vcfs


# ─────────────────────────────────────────────────────────────────────────────
# Mutation filtering helpers  (step 9)
# ─────────────────────────────────────────────────────────────────────────────

def _find_repeats(seq: str, min_unit: int = 1, max_unit: int = 6,
                  min_rep: int = 3) -> list:
    """
    Detect tandem repeat units in a sequence string.

    Scans every possible unit length from min_unit to max_unit.
    A repeat is recorded only when the unit appears at least min_rep times
    consecutively.  Returns (start, end, unit_seq, count) tuples (0-based).
    """
    found, n = [], len(seq)
    for ul in range(min_unit, max_unit + 1):
        i = 0
        while i <= n - ul:
            unit  = seq[i:i + ul]
            count = 1
            j     = i + ul
            while j + ul <= n and seq[j:j + ul] == unit:
                count += 1
                j     += ul
            if count >= min_rep:
                found.append((i, j, unit, count))
                i = j
            else:
                i += 1
    return found


def _classify_repeat(seq: str, pos: int):
    """
    Classify a variant position (1-based) relative to tandem repeats.

    Returns (repeat_region, repeat_count, ref_pos_in_unit, next_to_repeat).
    All four values are strings; "No" means the field does not apply.
    """
    rr = rc = rp = nr = "No"
    repeats = _find_repeats(seq)
    for s, e, unit, cnt in repeats:
        if s + 1 <= pos <= e:
            offset = (pos - (s + 1)) % len(unit)
            return seq[s:e], str(cnt), str(offset + 1), nr
    for s, e, unit, cnt in repeats:
        if pos == s or pos == e + 1:
            nr = "Yes"; rr = seq[s:e]; rc = str(cnt); break
    return rr, rc, rp, nr


def _repeat_filter_table(table: Path, mode: str,
                         out: Path, fp_out: Path, cfg: Config) -> None:
    """
    Partition a GATK VariantsToTable file into true candidates and likely
    false positives based on tandem-repeat context.   [main env for samtools]

    For each variant a ±100 bp window is fetched from the reference with
    samtools faidx (main env) and scanned for tandem repeats.

    Decision rules:
        SNP  : false positive if inside a repeat with count ≥ 10
        INDEL : false positive if inside any repeat region
    """
    header = (
        "CHROM\tPOS\tREF\tALT\tExtracted_REF\tRef_seq_marked\t"
        "RepeatRegion\tRepeatCount\tREFpos_inRepeatUnit\tNextToRepeat\n"
    )
    # Build the samtools faidx command prefix for main env
    faidx_prefix = (
        ["conda", "run", "-n", cfg.main_env, "--no-capture-output"]
        if cfg.main_env else []
    )

    with open(table) as fin, open(out, "w") as fpass, open(fp_out, "w") as ffail:
        fpass.write(header)
        ffail.write(header)
        col: dict = {}
        for lineno, raw in enumerate(fin):
            row = raw.rstrip("\n").split("\t")
            if lineno == 0:
                col = {h: i for i, h in enumerate(row)}
                continue
            chrom = row[col["CHROM"]]
            pos   = int(row[col["POS"]])
            ref_a = row[col["REF"]]
            alt   = row[col["ALT"]]

            start = max(1, pos - 100)
            end   = pos + 100
            res   = subprocess.run(
                faidx_prefix + [
                    "samtools", "faidx", str(cfg.ref),
                    f"{chrom}:{start}-{end}",
                ],
                capture_output=True, text=True,
            )
            seq = "".join(
                l for l in res.stdout.splitlines() if not l.startswith(">")
            )
            if not seq:
                line = (f"{chrom}\t{pos}\t{ref_a}\t{alt}"
                        "\tNo\tNo\tNo\tNo\tNo\tNo\n")
                fpass.write(line); ffail.write(line); continue

            idx    = pos - start + 1
            ext    = seq[idx - 1] if idx <= len(seq) else "?"
            marked = f"{seq[:idx-1]}[{seq[idx-1:idx]}]{seq[idx:]}"
            rr, rc, rp, nr = _classify_repeat(seq, idx)

            line = (f"{chrom}\t{pos}\t{ref_a}\t{alt}\t"
                    f"{ext}\t{marked}\t{rr}\t{rc}\t{rp}\t{nr}\n")
            is_fp = (
                (mode == "SNP"   and rr != "No"
                 and (rc == "No" or int(rc) >= 10)) or
                (mode == "INDEL" and rr != "No")
            )
            (ffail if is_fp else fpass).write(line)


def _gatk_filter_and_table(vcf_gz: Path, vtype: str,
                            out_dir: Path, cfg: Config) -> None:
    """
    Extract one variant type, apply hard quality filters, export to table.

    GATK commands  → base env  (SelectVariants, VariantFiltration, VariantsToTable)
    bgzip / tabix  → main env

    SNP  filters : QD < 2 | DP < 10 | SOR > 3  | FS > 60  | MQ < 50
    INDEL filters : QD < 2 | DP < 10 | FS > 200 | MQ < 50
    """
    base_name = vcf_gz.name[:-7]   # strip ".vcf.gz"
    sfx  = "snp" if vtype == "SNP" else "indels"
    sel  = out_dir / f"{base_name}_{sfx}.vcf"
    filt = out_dir / f"{base_name}_{sfx}_filtered.vcf"

    if vtype == "SNP":
        fname = "QD2DP10SOR3FS60MQ50"
        fexpr = "QD < 2.0 || DP < 10.0 || SOR > 3.0 || FS > 60.0 || MQ < 50.0"
    else:
        fname = "QD2DP10FS200MQ50"
        fexpr = "QD < 2.0 || DP < 10.0 || FS > 200.0 || MQ < 50.0"

    with conda_env_block("base", f"GATK {vtype} SelectVariants + VariantFiltration"):
        run_gatk([
            "SelectVariants",
            "-R", str(cfg.ref), "-V", str(vcf_gz),
            "--select-type-to-include", vtype,
            "-O", str(sel),
        ], step=f"select-{vtype}", cfg=cfg)

        run_gatk([
            "VariantFiltration",
            "-R", str(cfg.ref), "-V", str(sel),
            "-O", str(filt),
            "--filter-name", fname,
            "--filter-expression", fexpr,
        ], step=f"filter-{vtype}", cfg=cfg)

    sel.unlink(missing_ok=True)

    # Compress/index in main env
    gz = compress_and_index(filt, step=f"compress-{vtype}", cfg=cfg)

    tbl_dir = out_dir / "Table"
    tbl_dir.mkdir(exist_ok=True)

    with conda_env_block("base", f"GATK {vtype} VariantsToTable"):
        run_gatk([
            "VariantsToTable",
            "-V", str(gz),
            "-F", "CHROM", "-F", "POS",    "-F", "QUAL",
            "-F", "REF",   "-F", "ALT",    "-F", "TYPE",
            "-F", "FILTER","-F", "FS",     "-F", "SOR",
            "-GF", "AF", "-GF", "AD", "-GF", "GT",
            "-GF", "GQ", "-GF", "SB",
            "-O", str(tbl_dir / gz.name.replace(".vcf.gz", ".table")),
        ], step=f"variants-to-table-{vtype}", cfg=cfg)


# ─────────────────────────────────────────────────────────────────────────────
# Step 9 — Mutation filtering
# ─────────────────────────────────────────────────────────────────────────────

def step9_mutation_filter(cfg: Config) -> None:
    """
    Step 9 — Three-stage mutation filtering.

    9a. Ancestral variant removal (bcftools isec)   [main env]
        Subtracts every ancestor VCF in sequence.  Works for both mode A
        (pre-existing VCFs) and mode B (VCFs built in the ancestor sub-run).

    9b-9d. GATK quality filtering                  [base env]
        SNPs and INDELs are separated, hard quality filters applied, and
        passing variants exported to tab-delimited tables.

    9e. Tandem-repeat region filtering              [main env — samtools]
        Each variant's ±100 bp reference context is scanned for tandem
        repeats.  SNPs in high-count repeats (≥ 10×) and INDELs in any
        repeat are written to *_falsepos.tsv; candidates go to *_output.tsv.
    """
    anc_dir = cfg.variants_dir / "Filtered_against_ancestors"
    snp_dir = cfg.variants_dir / "SNP"
    ind_dir = cfg.variants_dir / "INDELS"
    mkdirs(anc_dir, snp_dir, ind_dir)

    # ── 9a: ancestor subtraction   [main env] ────────────────────────────────
    sample_vcfs = (sorted(cfg.vcf_dir.glob("*.vcf")) +
                   sorted(cfg.vcf_dir.glob("*.vcf.gz")))

    with conda_env_block(cfg.main_env or "current shell", "bcftools isec"):
        for vcf in sample_vcfs:
            vcf_gz  = (compress_and_index(vcf, step="9-prep", cfg=cfg)
                       if vcf.suffix == ".vcf" else vcf)
            current = vcf_gz

            for j, anc_vcf in enumerate(cfg.ancestor_vcfs):
                anc_gz = (compress_and_index(anc_vcf, step=f"9-idx-anc{j}", cfg=cfg)
                          if anc_vcf.suffix == ".vcf" else anc_vcf)

                isec_dir = cfg.variants_dir / f"{vcf_gz.stem}_anc{j}_isec"
                run_main([
                    "bcftools", "isec",
                    "-p", str(isec_dir), "-Oz",
                    str(anc_gz), str(current),
                ], step=f"9a-isec-anc{j}", cfg=cfg)

                is_last = (j == len(cfg.ancestor_vcfs) - 1)
                dest = (anc_dir / f"{vcf_gz.stem}_anc.vcf.gz") if is_last \
                       else (cfg.variants_dir / f"{vcf_gz.stem}_pass{j}.vcf.gz")

                (isec_dir / "0001.vcf.gz").rename(dest)
                compress_and_index(dest, step=f"9a-idx-pass{j}", cfg=cfg)
                subprocess.run(["rm", "-rf", str(isec_dir)])

                if j > 0:
                    current.unlink(missing_ok=True)
                    Path(str(current) + ".tbi").unlink(missing_ok=True)
                current = dest

    # ── 9b-9d: GATK quality filtering   [base env] ───────────────────────────
    for anc_vcf in sorted(anc_dir.glob("*_anc.vcf.gz")):
        for vtype, odir in [("SNP", snp_dir), ("INDEL", ind_dir)]:
            _gatk_filter_and_table(anc_vcf, vtype, odir, cfg)

    # ── 9e: repeat-region filtering   [main env — samtools faidx] ────────────
    for mode, tbl_dir in [("SNP",   snp_dir / "Table"),
                           ("INDEL", ind_dir  / "Table")]:
        for tbl in sorted(tbl_dir.glob("*filtered.table")):
            out    = tbl.with_name(tbl.stem + "_output.tsv")
            fp_out = tbl.with_name(tbl.stem + "_falsepos.tsv")
            log.info(f"  Repeat filter [{mode}]: {tbl.name}")
            _repeat_filter_table(tbl, mode, out, fp_out, cfg)
            log.info(f"    ✓ {out.name}  |  {fp_out.name}")


# ─────────────────────────────────────────────────────────────────────────────
# Main pipeline orchestrator  (steps 1-9)
# ─────────────────────────────────────────────────────────────────────────────

STEP_NAMES = {
    1: "Quality trimming          (Trimmomatic)                    [main env]",
    2: "Index reference genome    (BWA + samtools faidx + Picard)  [main+base]",
    3: "Align reads + sort to BAM (BWA MEM + SortSam)              [main env]",
    4: "Index sorted BAMs         (Picard BuildBamIndex)            [main env]",
    5: "Mark duplicates           (Picard MarkDuplicates)           [main env]",
    6: "Fix read groups           (Picard AddOrReplaceReadGroups)   [main env]",
    7: "Index fixed BAMs          (samtools)                        [main env]",
    8: "Variant calling           (GATK HaplotypeCaller)            [base env]",
    9: "Mutation filtering        (bcftools + GATK + Python)        [main+base]",
}


def run_main_pipeline(cfg: Config) -> None:
    for n in range(cfg.start_step, 10):
        log.info(f"{'─' * 60}")
        log.info(f"Step {n}: {STEP_NAMES[n]}")

        if n == 1:
            run_trimmomatic(cfg.raw_dir, cfg.trimmed_paired,
                            cfg.trimmed_unpaired, cfg)
        elif n == 2:
            if cfg.skip_index:
                log.info("  --skip-index set; skipping BWA index.")
            else:
                run_index_reference(cfg)
        elif n == 3:
            run_align_and_sort(cfg.trimmed_paired, cfg.sorted_dir,
                               cfg.aligned_dir, cfg)
        elif n == 4:
            run_index_bam(cfg.sorted_dir, cfg)
        elif n == 5:
            run_mark_duplicates(cfg.sorted_dir, cfg.marked_dir, cfg)
        elif n == 6:
            run_fix_read_groups(cfg.marked_dir, cfg.fixed_rg_dir, cfg)
        elif n == 7:
            run_index_fixed_bams(cfg.fixed_rg_dir, cfg)
        elif n == 8:
            run_call_variants(cfg.fixed_rg_dir, cfg.vcf_dir, cfg)
        elif n == 9:
            if cfg.ancestor_mode == "b":
                cfg.ancestor_vcfs    = process_ancestor_fastqs(cfg)
                cfg.ancestor_vcf_dir = cfg.ancestor_project / "5.Variants_call"
            step9_mutation_filter(cfg)

        log.info(f"Step {n} complete.")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        prog="genomic_variant_pipeline.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # ── Required paths ───────────────────────────────────────────────────────
    req = p.add_argument_group("required paths")
    req.add_argument("--project-dir", required=True, type=Path, metavar="DIR",
                     help="Root output directory (created if absent). "
                          "Place raw FASTQs in <DIR>/Raw/.")
    req.add_argument("--ref-dir",  required=True, type=Path, metavar="DIR",
                     help="Directory containing the reference genome FASTA.")
    req.add_argument("--ref-name", required=True, metavar="FILENAME",
                     help="FASTA filename inside --ref-dir  (e.g. genome_v1.fa).")

    # ── Conda environment ────────────────────────────────────────────────────
    envs = p.add_argument_group(
        "conda environment",
        "GATK is expected in the conda base environment and is always called\n"
        "via 'conda run -n base', regardless of which environment this script\n"
        "was started from.\n\n"
        "All other tools (Trimmomatic, BWA, Picard, samtools, bcftools,\n"
        "bgzip, tabix) are called via 'conda run -n <main-env>' when\n"
        "--main-env is provided, or directly from PATH if omitted.\n\n"
        "This applies to both the main sample run and the ancestor sub-run\n"
        "(Mode B), so a single --main-env flag covers the entire pipeline."
    )
    envs.add_argument(
        "--main-env", metavar="NAME", default=None,
        help="Conda environment containing non-GATK tools "
             "(Trimmomatic, BWA, Picard, samtools, bcftools, bgzip, tabix). "
             "Example: --main-env genome-analysis. "
             "Omit if all tools are already on PATH in the active shell.",
    )

    # ── Ancestor mode ────────────────────────────────────────────────────────
    anc = p.add_argument_group(
        "ancestor options  (choose one mode)",
        "Mode A — use pre-existing VCF files:\n"
        "    --ancestor-vcf-dir /path/to/vcf_folder\n"
        "    --ancestor-vcf     file1.vcf.gz   (repeat for each file)\n\n"
        "Mode B — generate ancestor VCFs from raw FASTQ files:\n"
        "    --ancestor-fastq-dir /path/to/ancestor_reads\n"
        "    FASTQs must follow the *_R1_001.fastq.gz naming convention.\n"
        "    Steps 1-8 run on these files using the same --main-env and\n"
        "    base-env layout as the main sample pipeline."
    )
    anc.add_argument("--ancestor-vcf-dir", type=Path, metavar="DIR",
                     help="[Mode A] Folder containing pre-built ancestor VCFs.")
    anc.add_argument("--ancestor-vcf", action="append", metavar="FILENAME",
                     help="[Mode A] VCF filename inside --ancestor-vcf-dir. "
                          "Repeat for multiple ancestors.")
    anc.add_argument("--ancestor-fastq-dir", type=Path, metavar="DIR",
                     help="[Mode B] Folder of paired ancestor FASTQ files. "
                          "Pipeline runs steps 1-8 on these (using --main-env "
                          "and base), then uses the VCFs for filtering.")

    # ── Run options ──────────────────────────────────────────────────────────
    run_opts = p.add_argument_group("run options")
    run_opts.add_argument("--ploidy", type=int, default=2,
                          help="Organism ploidy for HaplotypeCaller (default: 2).")
    run_opts.add_argument("--threads", type=int, default=8,
                          help="CPU threads for BWA MEM and GATK (default: 8).")
    run_opts.add_argument("--skip-index", action="store_true",
                          help="Skip BWA reference indexing (step 2) if already done.")
    run_opts.add_argument("--start-step", type=int, default=1,
                          choices=range(1, 10), metavar="{1-9}",
                          help="Resume the pipeline from this step (default: 1).")

    # ── Trimmomatic options ──────────────────────────────────────────────────
    trim = p.add_argument_group("trimmomatic options")
    trim.add_argument("--trim-leading",   type=int, default=3)
    trim.add_argument("--trim-trailing",  type=int, default=3)
    trim.add_argument("--trim-window",    type=int, default=4,
                      help="Sliding window size (default: 4).")
    trim.add_argument("--trim-quality",   type=int, default=20,
                      help="Min avg quality in sliding window (default: 20).")
    trim.add_argument("--trim-minlen",    type=int, default=36,
                      help="Discard reads shorter than N bp after trimming (default: 36).")
    trim.add_argument("--trim-headcrop",  type=int, default=15,
                      help="Remove N bases from 5' end (default: 15).")
    trim.add_argument("--trim-crop",      type=int, default=150,
                      help="Hard-clip reads to max N bp (default: 150).")

    args = p.parse_args()

    # Validate ancestor mode mutual exclusivity
    has_a = bool(args.ancestor_vcf_dir or args.ancestor_vcf)
    has_b = bool(args.ancestor_fastq_dir)
    if has_a and has_b:
        p.error("Specify either Mode A (--ancestor-vcf-dir/--ancestor-vcf) "
                "or Mode B (--ancestor-fastq-dir), not both.")
    if not has_a and not has_b:
        p.error("An ancestor source is required. See --help for Mode A / Mode B.")
    if has_a and not args.ancestor_vcf_dir:
        p.error("--ancestor-vcf-dir is required with --ancestor-vcf.")
    if has_a and not args.ancestor_vcf:
        p.error("At least one --ancestor-vcf filename is required.")

    return args


def main():
    args = parse_args()
    cfg  = Config(args)
    mkdirs(cfg.project_dir)
    setup_logging(cfg.project_dir / "pipeline.log")

    log.info("=" * 60)
    log.info("Genomic Variant Calling Pipeline")
    log.info("=" * 60)
    log.info(f"Project dir    : {cfg.project_dir}")
    log.info(f"Reference      : {cfg.ref}")
    log.info(f"Ploidy         : {cfg.ploidy}")
    log.info(f"Threads        : {cfg.threads}")
    log.info(f"Main env       : {cfg.main_env or '(current shell / PATH)'}")
    log.info(f"GATK env       : base  (always)")
    log.info(f"Ancestor mode  : "
             f"{'A — pre-existing VCFs' if cfg.ancestor_mode == 'a' else 'B — process FASTQ files'}")
    if cfg.ancestor_mode == "a":
        for v in cfg.ancestor_vcfs:
            log.info(f"  Ancestor VCF : {v}")
    else:
        log.info(f"  Ancestor dir : {cfg.ancestor_fastq_dir}")
    log.info(f"Start step     : {cfg.start_step}")
    log.info("=" * 60)

    cfg.validate()
    run_main_pipeline(cfg)

    log.info("=" * 60)
    log.info("Pipeline complete.")
    log.info(f"  SNP results   : {cfg.variants_dir}/SNP/Table/")
    log.info(f"  INDEL results : {cfg.variants_dir}/INDELS/Table/")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
