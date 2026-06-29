# Genomic analysis Pipeline

**Genomics · Python · GATK**

From raw reads to **filtered variants**

A generalizable end-to-end pipeline that takes paired-end FASTQ files from any organism and any reference genome through quality control, alignment, duplicate marking, variant calling, and multi-stage filtering—down to a clean SNP and INDEL table.

---

## Table of Contents

- [Overview](#overview)
- [Pipeline Workflow](#pipeline-workflow)
- [Requirements](#requirements)
- [Pipeline Steps](#pipeline-steps)
- [Usage](#usage)
- [Script](#script)

---

## Overview

This pipeline wraps nine sequential stages—from raw Illumina paired-end reads all the way to filtered, repeat-region-aware SNP and INDEL tables—into a single Python script.

Every path, ploidy, thread count, and ancestor VCF set is configurable from the command line, making it portable across projects and organisms.

---

## Pipeline Workflow

```mermaid
flowchart TD

A[Raw FASTQ Reads]

A --> B[Quality Trimming<br/>Trimmomatic]

R[Index Reference<br/>BWA index]

B --> C[Align Reads + Sort BAM]
R --> C

C --> D[Index BAMs]
D --> E[Mark Duplicates]
E --> F[Fix Read Groups]
F --> G[Index Fixed BAMs]

G --> H[Variant Calling<br/>GATK HaplotypeCaller]

H --> I[Remove Ancestral Variants]

I --> J[SNP Filtering]
I --> K[INDEL Filtering]

J --> L[Filtered SNPs TSV]
K --> M[Filtered INDELs TSV]

L --> N[Manual Filtering]
M --> N
```

---

## Requirements

| Tool | Purpose |
|--------|--------|
| Python ≥ 3.10 | Pipeline driver |
| Trimmomatic | Read quality trimming |
| BWA | Genome alignment |
| Picard | SAM/BAM processing |
| samtools | BAM indexing |
| GATK 4 | Variant calling & filtering |
| bcftools | Ancestor subtraction |
| bgzip / tabix | VCF compression & indexing |

---

## Pipeline Steps

### 1. Quality Trimming

**Tool:** Trimmomatic

- Removes adapters and low-quality bases.
- Sliding-window trimming (4 bp window, Q20).
- Discards reads shorter than 36 bp.
- Configurable via:

```bash
--minlen
--headcrop
```

---

### 2. Index Reference Genome

**Tool:** BWA

Builds the BWT/SA index required for alignment.

```bash
bwa index -a bwtsw reference.fa
```

Optional:

```bash
--skip-index
```

---

### 3. Align Reads and Sort BAM

**Tools:** BWA MEM + Picard SortSam

- Align paired-end reads.
- Convert SAM → coordinate-sorted BAM.
- Remove intermediate SAM files.

---

### 4. Index Sorted BAMs

**Tool:** Picard BuildBamIndex

Creates:

```text
sample_sorted.bam.bai
```

Required for downstream GATK processing.

---

### 5. Mark Duplicates

**Tool:** Picard MarkDuplicates

- Identifies PCR and optical duplicates.
- Generates duplication metrics.
- Duplicate reads remain flagged, not removed.

---

### 6. Fix Read Groups

**Tool:** Picard AddOrReplaceReadGroups

Adds:

```text
RGID
RGLB
RGPL
RGPU
RGSM
```

required by GATK.

---

### 7. Index Fixed BAMs

**Tool:** samtools index

Creates a fresh BAM index after read-group modification.

---

### 8. Variant Calling

**Tool:** GATK HaplotypeCaller

Configurable ploidy:

```bash
--ploidy 2
```

Annotations added:

- FisherStrand (FS)
- StrandOddsRatio (SOR)
- AlleleFraction (AF)

Outputs:

```text
sample.vcf.gz
sample.vcf.gz.tbi
```

---

### 9. Mutation Filtering

#### Stage A: Remove Ancestral Variants

```bash
bcftools isec
```

Subtracts variants found in one or more ancestor VCFs.

#### Stage B: Separate SNPs and INDELs

```bash
gatk SelectVariants
```

#### Stage C: Hard Filtering

SNP filters:

```text
QD < 2
DP < 10
SOR > 3
FS > 60
MQ < 50
```

INDEL filters:

```text
QD < 2
DP < 10
FS > 200
MQ < 50
```

#### Stage D: Repeat-Based Filtering

- SNPs in repeat regions with repeat count ≥10 flagged as false positives.
- INDELs inside repeat regions flagged as false positives.

#### Stage E: Manual Filtering

- Final step of filtering SNPs and INDELs by using IGV visualization to check ambiguous variants.

---

## Usage examples
--------------
Mode A — pre-existing VCFs:
    Pass --ancestor-vcf-dir and one or more --ancestor-vcf filenames.
    The pipeline uses those VCFs directly in step 9 filtering.

Mode B — raw FASTQ ancestors:
    Pass --ancestor-fastq-dir pointing to a folder of paired-end FASTQ files.
    Steps 1-8 are run on those files first (in <project-dir>/Ancestor/),
    then the resulting VCFs are used for filtering.
    Both modes fully support the base-vs-main-env layout described above.

### GATK in base, other tools in genome-analysis env, Mode A ancestors

```bash
python genomic_analysis_pipeline.py \
    --project-dir      /data/project \
    --ref-dir          /refs/genome_dir \
    --ref-name         genome_v1.fa \
    --main-env         genome-analysis \
    --ancestor-vcf-dir /refs/ancestor_vcfs \
    --ancestor-vcf     PM_t0.vcf.gz \
    --ancestor-vcf     PA_t0.vcf.gz \
    --ploidy 4 --threads 2
```

### Same layout, Mode B — pipeline processes ancestor FASTQs first

```bash
python genomic_analysis_pipeline.py \
    --project-dir        /data/project \
    --ref-dir            /refs/genome_dir \
    --ref-name           genome_v1.fa \
    --main-env           genome-analysis \
    --ancestor-fastq-dir /data/ancestor_reads \
    --ploidy 4 --threads 20
```

### All tools in one environment (no --main-env needed)

```bash
python genomic_analysis_pipeline.py \
    --project-dir      /data/project \
    --ref-dir          /refs/genome_dir \
    --ref-name         genome_v1.fa \
    --ancestor-vcf-dir /refs/ancestor_vcfs \
    --ancestor-vcf     ancestor.vcf.gz \
    --ploidy 2 --threads 8
```
## Outputs

```text
Filtered_against_ancestors/
SNP/
INDELS/
```

Final deliverables:

```text
*_output.tsv
*_falsepos.tsv
```
containing filtered SNP and INDEL calls and repeat-region false-positive classifications.

---
## License

Add your preferred license here.
