<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Genomic Variant Calling Pipeline</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Syne:wght@700;800&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --c-bg:        #f7f6f2;
    --c-surface:   #ffffff;
    --c-border:    #e2e0d8;
    --c-text:      #1a1a18;
    --c-muted:     #6b6b65;
    --c-accent:    #2c5f6e;
    --c-accent-lt: #AEC6CF;

    --c-input:   #E8E8E4;
    --c-preproc: #AEC6CF;
    --c-detect:  #FCD5CE;
    --c-filter:  #E4F4E3;
    --c-output:  #FAEDCB;

    --font-sans:  'Inter', sans-serif;
    --font-disp:  'Syne', sans-serif;
    --font-mono:  'IBM Plex Mono', monospace;

    --radius:  8px;
    --radius-lg: 12px;
  }

  html { scroll-behavior: smooth; }

  body {
    font-family: var(--font-sans);
    background: var(--c-bg);
    color: var(--c-text);
    font-size: 16px;
    line-height: 1.7;
  }

  /* ── NAV ── */
  nav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(247,246,242,0.92);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--c-border);
    padding: 0 2rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 56px;
  }
  .nav-brand {
    font-family: var(--font-mono);
    font-size: 13px; font-weight: 500;
    color: var(--c-accent);
    letter-spacing: 0.04em;
    text-decoration: none;
  }
  .nav-links { display: flex; gap: 2rem; list-style: none; }
  .nav-links a {
    font-size: 13px; color: var(--c-muted);
    text-decoration: none; letter-spacing: 0.02em;
    transition: color 0.15s;
  }
  .nav-links a:hover { color: var(--c-text); }

  /* ── HERO ── */
  .hero {
    max-width: 1100px; margin: 0 auto;
    padding: 72px 2rem 48px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: start;
  }
  .hero-text { padding-top: 8px; }
  .eyebrow {
    font-family: var(--font-mono);
    font-size: 11px; font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--c-accent);
    margin-bottom: 16px;
  }
  h1 {
    font-family: var(--font-disp);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800;
    line-height: 1.1;
    color: var(--c-text);
    margin-bottom: 20px;
    letter-spacing: -0.02em;
  }
  h1 span { color: var(--c-accent); }
  .hero-desc {
    font-size: 16px; color: var(--c-muted);
    max-width: 420px; margin-bottom: 32px;
    line-height: 1.75;
  }
  .btn-row { display: flex; gap: 12px; flex-wrap: wrap; }
  .btn {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 10px 20px; border-radius: var(--radius);
    font-size: 13px; font-weight: 500; letter-spacing: 0.02em;
    text-decoration: none; cursor: pointer;
    transition: opacity 0.15s, transform 0.15s;
    border: none;
  }
  .btn:hover { opacity: 0.85; transform: translateY(-1px); }
  .btn-primary { background: var(--c-accent); color: #fff; }
  .btn-secondary { background: var(--c-surface); color: var(--c-text); border: 1px solid var(--c-border); }

  /* diagram card */
  .diagram-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 20px 16px 12px;
    overflow: hidden;
  }
  .diagram-card svg { display: block; width: 100%; height: auto; }

  /* ── MAIN CONTENT ── */
  main { max-width: 1100px; margin: 0 auto; padding: 0 2rem 80px; }

  /* section titles */
  .section-head {
    display: flex; align-items: baseline; gap: 16px;
    margin: 64px 0 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--c-border);
  }
  .section-head h2 {
    font-family: var(--font-disp);
    font-size: 1.5rem; font-weight: 700;
    letter-spacing: -0.01em;
  }
  .section-tag {
    font-family: var(--font-mono);
    font-size: 11px; color: var(--c-muted);
    letter-spacing: 0.08em; text-transform: uppercase;
  }

  /* ── REQUIREMENTS ── */
  .req-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  .req-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius);
    padding: 14px 16px;
  }
  .req-card .tool-name {
    font-family: var(--font-mono);
    font-size: 13px; font-weight: 500; color: var(--c-accent);
  }
  .req-card .tool-role { font-size: 12px; color: var(--c-muted); margin-top: 2px; }

  /* ── STEPS ── */
  .steps { display: flex; flex-direction: column; gap: 12px; }
  .step-row {
    display: grid;
    grid-template-columns: 28px 1fr;
    gap: 16px;
    align-items: start;
  }
  .step-num {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    flex-shrink: 0; margin-top: 2px;
  }
  .step-body {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius);
    padding: 14px 18px;
  }
  .step-title {
    font-weight: 600; font-size: 14px; margin-bottom: 4px;
  }
  .step-desc { font-size: 13px; color: var(--c-muted); line-height: 1.6; }
  .step-tag {
    display: inline-block; margin-top: 8px;
    font-family: var(--font-mono); font-size: 11px;
    background: var(--c-bg); border: 1px solid var(--c-border);
    border-radius: 4px; padding: 2px 7px; color: var(--c-muted);
  }

  /* step color bands */
  .s-input  .step-num { background: var(--c-input);  color: #444; }
  .s-pre    .step-num { background: var(--c-preproc); color: #1d4a54; }
  .s-detect .step-num { background: var(--c-detect);  color: #7a2e20; }
  .s-filter .step-num { background: var(--c-filter);  color: #205020; }
  .s-out    .step-num { background: var(--c-output);  color: #5a3e10; }

  .s-pre    .step-body { border-left: 3px solid var(--c-preproc); }
  .s-detect .step-body { border-left: 3px solid var(--c-detect); }
  .s-filter .step-body { border-left: 3px solid var(--c-filter); }
  .s-out    .step-body { border-left: 3px solid var(--c-output); }

  /* ── CODE BLOCK ── */
  .code-wrap {
    background: #1a1a1a;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid #333;
  }
  .code-toolbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 16px;
    background: #111;
    border-bottom: 1px solid #2a2a2a;
  }
  .code-label {
    font-family: var(--font-mono);
    font-size: 12px; color: #888;
  }
  .copy-btn {
    font-family: var(--font-mono);
    font-size: 11px; color: #888;
    background: #222; border: 1px solid #333;
    border-radius: 4px; padding: 4px 10px;
    cursor: pointer; transition: color 0.15s;
  }
  .copy-btn:hover { color: #fff; }
  pre {
    margin: 0; padding: 20px;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 12.5px;
    line-height: 1.7;
    color: #e2e2e0;
    max-height: 600px;
    overflow-y: auto;
  }
  .kw  { color: #c792ea; }
  .fn  { color: #82aaff; }
  .st  { color: #c3e88d; }
  .cm  { color: #546e7a; font-style: italic; }
  .nu  { color: #f78c6c; }

  /* ── USAGE BLOCK ── */
  .usage-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 4px;
  }
  .usage-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius);
    padding: 16px 18px;
  }
  .usage-card h4 {
    font-size: 13px; font-weight: 600; margin-bottom: 10px;
  }
  .usage-card code {
    display: block;
    font-family: var(--font-mono); font-size: 12px;
    color: var(--c-accent); background: var(--c-bg);
    border-radius: 4px; padding: 8px 10px;
    margin-bottom: 6px;
    white-space: pre-wrap; word-break: break-all;
  }
  .usage-card .note { font-size: 12px; color: var(--c-muted); }

  /* ── LEGEND ── */
  .legend {
    display: flex; flex-wrap: wrap; gap: 16px;
    margin-bottom: 20px;
  }
  .legend-item {
    display: flex; align-items: center; gap: 7px;
    font-size: 13px; color: var(--c-muted);
  }
  .legend-dot {
    width: 13px; height: 13px; border-radius: 3px; flex-shrink: 0;
  }

  /* ── FOOTER ── */
  footer {
    border-top: 1px solid var(--c-border);
    padding: 28px 2rem;
    text-align: center;
    font-size: 12px; color: var(--c-muted);
    font-family: var(--font-mono);
  }

  /* ── RESPONSIVE ── */
  @media (max-width: 760px) {
    .hero {
      grid-template-columns: 1fr;
      gap: 2rem; padding: 40px 1.25rem 32px;
    }
    .usage-grid { grid-template-columns: 1fr; }
    nav { padding: 0 1.25rem; }
    .nav-links { gap: 1.2rem; }
    main { padding: 0 1.25rem 60px; }
  }

  @media (prefers-reduced-motion: reduce) {
    .btn { transition: none; }
  }
</style>
</head>
<body>

<nav>
  <a class="nav-brand" href="#">variant-pipeline</a>
  <ul class="nav-links">
    <li><a href="#overview">Overview</a></li>
    <li><a href="#steps">Steps</a></li>
    <li><a href="#script">Script</a></li>
    <li><a href="#usage">Usage</a></li>
  </ul>
</nav>

<!-- ── HERO ─────────────────────────────────────────── -->
<section class="hero">
  <div class="hero-text">
    <p class="eyebrow">Genomics · Python · GATK</p>
    <h1>From raw reads to <span>filtered variants</span></h1>
    <p class="hero-desc">
      A generalizable end-to-end pipeline that takes paired-end FASTQ files from any organism
      and any reference genome through quality control, alignment, duplicate marking,
      variant calling, and multi-stage filtering — down to a clean SNP and INDEL table.
    </p>
    <div class="btn-row">
      <a class="btn btn-primary" href="#script">View script</a>
      <a class="btn btn-secondary" href="#usage">Usage &amp; config</a>
    </div>
  </div>

  <div class="diagram-card">
    <svg viewBox="0 0 460 760" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pipeline flowchart">
      <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
        <style>
          .db { font-family:'Inter',sans-serif; font-weight:600; font-size:11px; }
          .ds { font-family:'Inter',sans-serif; font-weight:400; font-size:9.5px; fill:#555; }
          .dl { font-family:'Inter',sans-serif; font-weight:400; font-size:9px; fill:#888; }
          .t-pre { fill:#1d4a54; }
          .t-det { fill:#7a2e20; }
          .t-flt { fill:#205020; }
          .t-out { fill:#5a3e10; }
          .t-inp { fill:#3a3a38; }
        </style>
      </defs>

      <!-- Input -->
      <rect x="80" y="10" width="300" height="36" rx="7" fill="#E8E8E4" stroke="#9b9b95" stroke-width="0.7"/>
      <text class="db t-inp" x="230" y="32" text-anchor="middle">Raw FASTQ reads (paired-end)</text>

      <line x1="230" y1="46" x2="230" y2="62" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 1 -->
      <rect x="20" y="62" width="270" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="155" y="81" text-anchor="middle">Quality trimming</text>
      <text class="ds" x="155" y="97" text-anchor="middle">Trimmomatic PE · SLIDINGWINDOW · MINLEN</text>

      <!-- Step 2 (parallel) -->
      <rect x="308" y="62" width="132" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="374" y="80" text-anchor="middle">Index reference</text>
      <text class="ds" x="374" y="96" text-anchor="middle">BWA index -a bwtsw</text>

      <!-- merge lines into step 3 -->
      <line x1="155" y1="112" x2="155" y2="134" stroke="#999" stroke-width="2"/>
      <line x1="374" y1="112" x2="374" y2="128" stroke="#6a95a2" stroke-width="1.5" stroke-dasharray="4 2.5"/>
      <path d="M374 128 L374 138 L230 138 L230 148" fill="none" stroke="#6a95a2" stroke-width="1.5" stroke-dasharray="4 2.5"/>
      <path d="M155 134 L155 138 L230 138" fill="none" stroke="#999" stroke-width="2"/>
      <line x1="230" y1="138" x2="230" y2="148" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 3 -->
      <rect x="20" y="148" width="420" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="230" y="167" text-anchor="middle">Align reads + sort to BAM</text>
      <text class="ds" x="230" y="183" text-anchor="middle">BWA MEM → SAM · Picard SortSam → sorted BAM</text>

      <line x1="230" y1="198" x2="230" y2="214" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 4 -->
      <rect x="20" y="214" width="420" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="230" y="233" text-anchor="middle">Index sorted BAMs</text>
      <text class="ds" x="230" y="249" text-anchor="middle">Picard BuildBamIndex · generates .bai for random access</text>

      <line x1="230" y1="264" x2="230" y2="280" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 5 -->
      <rect x="20" y="280" width="420" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="230" y="299" text-anchor="middle">Mark duplicates</text>
      <text class="ds" x="230" y="315" text-anchor="middle">Picard MarkDuplicates · flags PCR/optical dups</text>

      <line x1="230" y1="330" x2="230" y2="346" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 6 -->
      <rect x="20" y="346" width="420" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="230" y="365" text-anchor="middle">Fix read groups</text>
      <text class="ds" x="230" y="381" text-anchor="middle">Picard AddOrReplaceReadGroups · RGID/RGLB/RGPL</text>

      <line x1="230" y1="396" x2="230" y2="412" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 7 -->
      <rect x="20" y="412" width="420" height="50" rx="7" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.7"/>
      <text class="db t-pre" x="230" y="431" text-anchor="middle">Index fixed BAMs</text>
      <text class="ds" x="230" y="447" text-anchor="middle">samtools index · fresh .bai after header change</text>

      <line x1="230" y1="462" x2="230" y2="478" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 8 -->
      <rect x="20" y="478" width="420" height="50" rx="7" fill="#FCD5CE" stroke="#d08070" stroke-width="0.7"/>
      <text class="db t-det" x="230" y="497" text-anchor="middle">Variant calling</text>
      <text class="ds" x="230" y="513" text-anchor="middle" style="fill:#9a4030">GATK HaplotypeCaller · ploidy N · FisherStrand · SOR</text>

      <line x1="230" y1="528" x2="230" y2="544" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- Step 9 outer box -->
      <rect x="10" y="544" width="440" height="176" rx="8" fill="none" stroke="#bbb" stroke-width="0.8" stroke-dasharray="4 2.5"/>
      <text class="dl" x="230" y="558" text-anchor="middle">Mutation filtering</text>

      <!-- 9a -->
      <rect x="20" y="564" width="420" height="42" rx="6" fill="#E4F4E3" stroke="#7ab878" stroke-width="0.7"/>
      <text class="db t-flt" x="230" y="580" text-anchor="middle">Ancestral variant removal</text>
      <text class="ds" x="230" y="595" text-anchor="middle" style="fill:#306830">bcftools isec · subtract ancestor VCFs</text>

      <line x1="230" y1="606" x2="230" y2="618" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- 9b split -->
      <rect x="20" y="618" width="200" height="40" rx="6" fill="#E4F4E3" stroke="#7ab878" stroke-width="0.7"/>
      <text class="db t-flt" x="120" y="633" text-anchor="middle">SNP quality filter</text>
      <text class="ds" x="120" y="648" text-anchor="middle" style="fill:#306830">QD · SOR · FS · MQ</text>

      <rect x="240" y="618" width="200" height="40" rx="6" fill="#E4F4E3" stroke="#7ab878" stroke-width="0.7"/>
      <text class="db t-flt" x="340" y="633" text-anchor="middle">INDEL quality filter</text>
      <text class="ds" x="340" y="648" text-anchor="middle" style="fill:#306830">QD · FS · MQ · DP</text>

      <line x1="120" y1="658" x2="120" y2="670" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>
      <line x1="340" y1="658" x2="340" y2="670" stroke="#999" stroke-width="2" marker-end="url(#arr)"/>

      <!-- outputs -->
      <rect x="20" y="670" width="200" height="36" rx="6" fill="#FAEDCB" stroke="#d4b86a" stroke-width="0.7"/>
      <text class="db t-out" x="120" y="693" text-anchor="middle">Filtered SNPs (.tsv)</text>

      <rect x="240" y="670" width="200" height="36" rx="6" fill="#FAEDCB" stroke="#d4b86a" stroke-width="0.7"/>
      <text class="db t-out" x="340" y="693" text-anchor="middle">Filtered INDELs (.tsv)</text>

      <!-- legend -->
      <rect x="20" y="728" width="11" height="11" rx="2" fill="#AEC6CF" stroke="#6a95a2" stroke-width="0.6"/>
      <text class="dl" x="35" y="738">Pre-processing</text>
      <rect x="130" y="728" width="11" height="11" rx="2" fill="#FCD5CE" stroke="#d08070" stroke-width="0.6"/>
      <text class="dl" x="145" y="738">Variant detection</text>
      <rect x="260" y="728" width="11" height="11" rx="2" fill="#E4F4E3" stroke="#7ab878" stroke-width="0.6"/>
      <text class="dl" x="275" y="738">Filtering</text>
      <rect x="330" y="728" width="11" height="11" rx="2" fill="#FAEDCB" stroke="#d4b86a" stroke-width="0.6"/>
      <text class="dl" x="345" y="738">Output</text>
    </svg>
  </div>
</section>

<!-- ── OVERVIEW ────────────────────────────────────────── -->
<main>
  <div id="overview" class="section-head">
    <h2>Overview</h2>
    <span class="section-tag">what it does</span>
  </div>

  <p style="color:var(--c-muted);max-width:680px;margin-bottom:24px;">
    This pipeline wraps nine sequential stages — from raw Illumina paired-end reads all the way to filtered,
    repeat-region-aware SNP and INDEL tables — into a single Python script. Every path,
    ploidy, thread count, and ancestor VCF set is configurable from the command line,
    making it portable across projects and organisms.
  </p>

  <div class="section-head">
    <h2>Requirements</h2>
    <span class="section-tag">tools &amp; versions</span>
  </div>

  <div class="req-grid">
    <div class="req-card"><div class="tool-name">Python ≥ 3.10</div><div class="tool-role">Pipeline driver</div></div>
    <div class="req-card"><div class="tool-name">Trimmomatic</div><div class="tool-role">Read quality trimming</div></div>
    <div class="req-card"><div class="tool-name">BWA</div><div class="tool-role">Genome alignment</div></div>
    <div class="req-card"><div class="tool-name">Picard</div><div class="tool-role">SAM/BAM processing</div></div>
    <div class="req-card"><div class="tool-name">samtools</div><div class="tool-role">BAM indexing</div></div>
    <div class="req-card"><div class="tool-name">GATK 4</div><div class="tool-role">Variant calling &amp; filtering</div></div>
    <div class="req-card"><div class="tool-name">bcftools</div><div class="tool-role">Ancestor subtraction</div></div>
    <div class="req-card"><div class="tool-name">bgzip / tabix</div><div class="tool-role">VCF compression &amp; indexing</div></div>
  </div>

  <!-- ── STEPS ── -->
  <div id="steps" class="section-head">
    <h2>Pipeline steps</h2>
    <span class="section-tag">9 stages</span>
  </div>

  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#AEC6CF;border:1px solid #6a95a2"></div>Pre-processing</div>
    <div class="legend-item"><div class="legend-dot" style="background:#FCD5CE;border:1px solid #d08070"></div>Variant detection</div>
    <div class="legend-item"><div class="legend-dot" style="background:#E4F4E3;border:1px solid #7ab878"></div>Variant filtering</div>
    <div class="legend-item"><div class="legend-dot" style="background:#FAEDCB;border:1px solid #d4b86a"></div>Output</div>
  </div>

  <div class="steps">
    <div class="step-row s-pre">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title">Quality trimming</div>
        <div class="step-desc">Trims adapter sequences and low-quality bases using Trimmomatic PE. Sliding-window trimming cuts when a 4-base window drops below Q20. Reads shorter than 36 bp post-trim are discarded. Configurable via <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">--minlen</code> and <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">--headcrop</code>.</div>
        <span class="step-tag">Trimmomatic</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title">Index reference genome <em style="font-weight:400;color:var(--c-muted);font-size:12px">(parallel)</em></div>
        <div class="step-desc">Builds the BWT/SA index BWA needs for rapid alignment. Uses the <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">bwtsw</code> algorithm for large genomes. Point <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">--ref</code> at any FASTA. Skip on re-runs with <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">--skip-index</code>.</div>
        <span class="step-tag">BWA</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">3</div>
      <div class="step-body">
        <div class="step-title">Align reads + sort to BAM</div>
        <div class="step-desc">Aligns trimmed paired-end reads to the reference with BWA MEM, then immediately coordinate-sorts the SAM output into BAM using Picard SortSam. Intermediate SAMs are deleted to save disk space.</div>
        <span class="step-tag">BWA MEM · Picard SortSam</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">4</div>
      <div class="step-body">
        <div class="step-title">Index sorted BAMs</div>
        <div class="step-desc">Generates a <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">.bai</code> index alongside each coordinate-sorted BAM, enabling random access required by Picard MarkDuplicates and GATK.</div>
        <span class="step-tag">Picard BuildBamIndex</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">5</div>
      <div class="step-body">
        <div class="step-title">Mark duplicates</div>
        <div class="step-desc">Identifies PCR and optical duplicates by comparing alignment start positions and strands. Duplicates are flagged but retained — GATK HaplotypeCaller skips them automatically. A per-sample metrics file reports the duplication rate.</div>
        <span class="step-tag">Picard MarkDuplicates</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">6</div>
      <div class="step-body">
        <div class="step-title">Fix read groups</div>
        <div class="step-desc">GATK requires <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">@RG</code> tags in BAM headers. This step writes RGID, RGLB, RGPL, RGPU, and RGSM fields. The sample name is derived automatically from the filename.</div>
        <span class="step-tag">Picard AddOrReplaceReadGroups</span>
      </div>
    </div>
    <div class="step-row s-pre">
      <div class="step-num">7</div>
      <div class="step-body">
        <div class="step-title">Index fixed BAMs</div>
        <div class="step-desc">Re-indexes the read-group-corrected BAMs. A fresh <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">.bai</code> is required after the header change in step 6.</div>
        <span class="step-tag">samtools index</span>
      </div>
    </div>
    <div class="step-row s-detect">
      <div class="step-num">8</div>
      <div class="step-body">
        <div class="step-title">Variant calling</div>
        <div class="step-desc">Calls SNPs and INDELs with GATK HaplotypeCaller. Ploidy is configurable via <code style="font-family:var(--font-mono);font-size:12px;background:var(--c-bg);padding:1px 5px;border-radius:3px">--ploidy</code> (default 2). Strand-bias annotations (FisherStrand, SOR, AlleleFraction) are added for downstream filtering. VCFs are bgzipped and tabix-indexed.</div>
        <span class="step-tag">GATK HaplotypeCaller</span>
      </div>
    </div>
    <div class="step-row s-filter">
      <div class="step-num">9</div>
      <div class="step-body">
        <div class="step-title">Mutation filtering</div>
        <div class="step-desc">Four-stage filter: <strong>(a)</strong> subtract variants present in any ancestor VCF via bcftools isec — any number of ancestor VCFs accepted; <strong>(b)</strong> separate SNPs and INDELs; <strong>(c)</strong> apply hard quality filters (QD, DP, SOR, FS, MQ); <strong>(d)</strong> classify variants in a ±100 bp reference window — SNPs in repeats with count ≥ 10 and all INDELs inside any repeat are flagged as false positives.</div>
        <span class="step-tag">bcftools · GATK · Python</span>
      </div>
    </div>
  </div>

  <!-- ── SCRIPT ── -->
  <div id="script" class="section-head">
    <h2>Script</h2>
    <span class="section-tag">genomic_variant_pipeline.py</span>
  </div>

  <div class="code-wrap">
    <div class="code-toolbar">
      <span class="code-label">genomic_variant_pipeline.py</span>
      <button class="copy-btn" onclick="copyCode()">Copy</button>
    </div>
    <pre id="code-block"><span class="cm">#!/usr/bin/env python3
"""
Genomic Variant Calling Pipeline
=================================
End-to-end pipeline: raw FASTQ → filtered SNP/INDEL tables.
Works with any reference genome and any set of ancestor VCFs.

Usage:
    python genomic_variant_pipeline.py \\
        --project-dir  /path/to/project \\
        --ref          /path/to/reference.fa \\
        --ancestor-vcf /path/to/ancestor1.vcf.gz \\
        --ancestor-vcf /path/to/ancestor2.vcf.gz \\
        --ploidy       2 \\
        --threads      16 \\
        [--skip-index] [--start-step N]

Requirements:
    trimmomatic, bwa, picard, samtools, gatk, bcftools, bgzip, tabix
"""</span>

<span class="kw">import</span> os, sys, subprocess, argparse, logging
<span class="kw">from</span> pathlib <span class="kw">import</span> Path

<span class="cm"># ── Logging ────────────────────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">setup_logging</span>(log_file: Path) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format=<span class="st">"%(asctime)s  %(levelname)-8s  %(message)s"</span>,
        datefmt=<span class="st">"%H:%M:%S"</span>,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(<span class="fn">str</span>(log_file), mode=<span class="st">"a"</span>),
        ],
    )
    <span class="kw">return</span> logging.getLogger(<span class="st">"pipeline"</span>)

log = logging.getLogger(<span class="st">"pipeline"</span>)

<span class="cm"># ── Utilities ──────────────────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">run</span>(cmd: list, step: str) -> <span class="kw">None</span>:
    <span class="st">"""Run a shell command; exit on failure."""</span>
    log.info(<span class="st">f"[{step}] {' '.join(str(c) for c in cmd)}"</span>)
    r = subprocess.run(cmd, capture_output=<span class="kw">True</span>, text=<span class="kw">True</span>)
    <span class="kw">if</span> r.stdout: log.info(r.stdout.strip())
    <span class="kw">if</span> r.stderr: log.warning(r.stderr.strip())
    <span class="kw">if</span> r.returncode != <span class="nu">0</span>:
        log.error(<span class="st">f"[{step}] failed (exit {r.returncode})"</span>)
        sys.exit(r.returncode)

<span class="kw">def</span> <span class="fn">mkdirs</span>(*dirs: Path) -> <span class="kw">None</span>:
    <span class="kw">for</span> d <span class="kw">in</span> dirs: d.mkdir(parents=<span class="kw">True</span>, exist_ok=<span class="kw">True</span>)

<span class="kw">def</span> <span class="fn">compress_index</span>(vcf: Path, step: str) -> Path:
    <span class="st">"""bgzip + tabix a VCF if not already done."""</span>
    gz = vcf.with_suffix(<span class="st">".vcf.gz"</span>) <span class="kw">if</span> vcf.suffix == <span class="st">".vcf"</span> <span class="kw">else</span> vcf
    <span class="kw">if</span> vcf.suffix == <span class="st">".vcf"</span> <span class="kw">and not</span> gz.exists():
        run([<span class="st">"bgzip"</span>, <span class="fn">str</span>(vcf)], step)
    <span class="kw">if not</span> Path(<span class="fn">str</span>(gz) + <span class="st">".tbi"</span>).exists():
        run([<span class="st">"tabix"</span>, <span class="fn">str</span>(gz)], step)
    <span class="kw">return</span> gz

<span class="cm"># ── Step 1 — Quality trimming ───────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step1_trimmomatic</span>(cfg) -> <span class="kw">None</span>:
    mkdirs(cfg.trimmed_paired, cfg.trimmed_unpaired)
    r1_files = <span class="fn">sorted</span>(cfg.raw_dir.glob(<span class="st">"*_R1_001.fastq.gz"</span>))
    <span class="kw">if not</span> r1_files:
        log.warning(<span class="st">"Step 1: no R1 files found — skipping."</span>); <span class="kw">return</span>
    <span class="kw">for</span> r1 <span class="kw">in</span> r1_files:
        stem = r1.name[:-<span class="nu">14</span>]
        r2   = r1.parent / (stem + <span class="st">"2_001.fastq.gz"</span>)
        run([
            <span class="st">"trimmomatic"</span>, <span class="st">"PE"</span>, <span class="st">"-phred33"</span>, <span class="fn">str</span>(r1), <span class="fn">str</span>(r2),
            <span class="fn">str</span>(cfg.trimmed_paired   / <span class="st">f"{stem}_paired.fastq"</span>),
            <span class="fn">str</span>(cfg.trimmed_unpaired / <span class="st">f"{stem}_unpaired.fastq"</span>),
            <span class="fn">str</span>(cfg.trimmed_paired   / <span class="st">f"{stem[:-1]}2_paired.fastq"</span>),
            <span class="fn">str</span>(cfg.trimmed_unpaired / <span class="st">f"{stem[:-1]}2_unpaired.fastq"</span>),
            <span class="st">f"LEADING:{cfg.trim_leading}"</span>,
            <span class="st">f"TRAILING:{cfg.trim_trailing}"</span>,
            <span class="st">f"SLIDINGWINDOW:{cfg.trim_window}:{cfg.trim_quality}"</span>,
            <span class="st">f"MINLEN:{cfg.trim_minlen}"</span>,
            <span class="st">f"HEADCROP:{cfg.trim_headcrop}"</span>,
            <span class="st">f"CROP:{cfg.trim_crop}"</span>,
        ], step=<span class="st">"1-trimmomatic"</span>)

<span class="cm"># ── Step 2 — Index reference genome ────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step2_index_reference</span>(cfg) -> <span class="kw">None</span>:
    run([<span class="st">"bwa"</span>, <span class="st">"index"</span>, <span class="st">"-a"</span>, <span class="st">"bwtsw"</span>, <span class="fn">str</span>(cfg.ref)], step=<span class="st">"2-bwa-index"</span>)

<span class="cm"># ── Step 3 — Align + sort ───────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step3_align_and_sort</span>(cfg) -> <span class="kw">None</span>:
    mkdirs(cfg.aligned_dir, cfg.sorted_dir)
    <span class="kw">for</span> r1 <span class="kw">in</span> <span class="fn">sorted</span>(cfg.trimmed_paired.glob(<span class="st">"*_R1_paired.fastq"</span>)):
        stem = r1.name.replace(<span class="st">"_R1_paired.fastq"</span>, <span class="st">""</span>)
        sam  = cfg.aligned_dir / <span class="st">f"{stem}.sam"</span>
        bam  = cfg.sorted_dir  / <span class="st">f"{stem}_sorted.bam"</span>
        run([<span class="st">"bwa"</span>, <span class="st">"mem"</span>, <span class="st">"-t"</span>, <span class="fn">str</span>(cfg.threads), <span class="fn">str</span>(cfg.ref),
             <span class="fn">str</span>(r1), <span class="fn">str</span>(cfg.trimmed_paired / <span class="st">f"{stem}_R2_paired.fastq"</span>),
             <span class="st">"-o"</span>, <span class="fn">str</span>(sam)], step=<span class="st">"3a-bwa-mem"</span>)
        run([<span class="st">"picard"</span>, <span class="st">"SortSam"</span>, <span class="st">f"INPUT={sam}"</span>, <span class="st">f"OUTPUT={bam}"</span>,
             <span class="st">"SORT_ORDER=coordinate"</span>], step=<span class="st">"3b-sortsam"</span>)
        sam.unlink(missing_ok=<span class="kw">True</span>)

<span class="cm"># ── Step 4 — Index sorted BAMs ──────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step4_index_bam</span>(cfg) -> <span class="kw">None</span>:
    <span class="kw">for</span> bam <span class="kw">in</span> <span class="fn">sorted</span>(cfg.sorted_dir.glob(<span class="st">"*sorted.bam"</span>)):
        run([<span class="st">"picard"</span>, <span class="st">"BuildBamIndex"</span>, <span class="st">f"INPUT={bam}"</span>], step=<span class="st">"4-index-bam"</span>)

<span class="cm"># ── Step 5 — Mark duplicates ────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step5_mark_duplicates</span>(cfg) -> <span class="kw">None</span>:
    mkdirs(cfg.marked_dir)
    <span class="kw">for</span> bam <span class="kw">in</span> <span class="fn">sorted</span>(cfg.sorted_dir.glob(<span class="st">"*_sorted.bam"</span>)):
        stem = bam.name[:-<span class="nu">10</span>]
        run([<span class="st">"picard"</span>, <span class="st">"MarkDuplicates"</span>, <span class="st">"VALIDATION_STRINGENCY=LENIENT"</span>,
             <span class="st">f"INPUT={bam}"</span>,
             <span class="st">f"OUTPUT={cfg.marked_dir / f'{stem}marked.bam'}"</span>,
             <span class="st">f"METRICS_FILE={cfg.marked_dir / f'{stem}metrics'}"</span>],
            step=<span class="st">"5-mark-dups"</span>)

<span class="cm"># ── Step 6 — Fix read groups ────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step6_fix_read_groups</span>(cfg) -> <span class="kw">None</span>:
    mkdirs(cfg.fixed_rg_dir)
    <span class="kw">for</span> bam <span class="kw">in</span> <span class="fn">sorted</span>(cfg.marked_dir.glob(<span class="st">"*_marked.bam"</span>)):
        stem = bam.name[:-<span class="nu">11</span>]
        run([<span class="st">"picard"</span>, <span class="st">"AddOrReplaceReadGroups"</span>, <span class="st">"VALIDATION_STRINGENCY=LENIENT"</span>,
             <span class="st">f"I={bam}"</span>, <span class="st">f"O={cfg.fixed_rg_dir / f'{stem}fixed.bam'}"</span>,
             <span class="st">"RGID=4"</span>, <span class="st">"RGLB=lib1"</span>, <span class="st">"RGPL=illumina"</span>, <span class="st">"RGPU=unit1"</span>,
             <span class="st">f"RGSM={stem}"</span>], step=<span class="st">"6-fix-rg"</span>)

<span class="cm"># ── Step 7 — Index fixed BAMs ───────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step7_index_fixed_bams</span>(cfg) -> <span class="kw">None</span>:
    <span class="kw">for</span> bam <span class="kw">in</span> <span class="fn">sorted</span>(cfg.fixed_rg_dir.glob(<span class="st">"*_fixed.bam"</span>)):
        run([<span class="st">"samtools"</span>, <span class="st">"index"</span>, <span class="fn">str</span>(bam)], step=<span class="st">"7-index-fixed"</span>)

<span class="cm"># ── Step 8 — Variant calling ────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">step8_call_variants</span>(cfg) -> <span class="kw">None</span>:
    mkdirs(cfg.vcf_dir)
    <span class="kw">for</span> bam <span class="kw">in</span> <span class="fn">sorted</span>(cfg.fixed_rg_dir.glob(<span class="st">"*_fixed.bam"</span>)):
        stem = bam.name[:-<span class="nu">10</span>]
        run([<span class="st">"gatk"</span>, <span class="st">"HaplotypeCaller"</span>,
             <span class="st">"--native-pair-hmm-threads"</span>, <span class="fn">str</span>(cfg.threads),
             <span class="st">"-I"</span>, <span class="fn">str</span>(bam), <span class="st">"-O"</span>, <span class="fn">str</span>(cfg.vcf_dir / <span class="st">f"{stem}.vcf"</span>),
             <span class="st">"-R"</span>, <span class="fn">str</span>(cfg.ref),
             <span class="st">"-A"</span>, <span class="st">"FisherStrand"</span>, <span class="st">"-A"</span>, <span class="st">"StrandBiasBySample"</span>,
             <span class="st">"-A"</span>, <span class="st">"StrandOddsRatio"</span>, <span class="st">"-A"</span>, <span class="st">"AlleleFraction"</span>,
             <span class="st">"--ploidy"</span>, <span class="fn">str</span>(cfg.ploidy)], step=<span class="st">"8-haplotypecaller"</span>)
    <span class="kw">for</span> v <span class="kw">in</span> <span class="fn">sorted</span>(cfg.vcf_dir.glob(<span class="st">"*.vcf"</span>)):
        compress_index(v, step=<span class="st">"8-compress"</span>)

<span class="cm"># ── Step 9 — Mutation filtering ─────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">_find_repeats</span>(seq: str, min_unit=<span class="nu">1</span>, max_unit=<span class="nu">6</span>, min_rep=<span class="nu">3</span>) -> list:
    out, n = [], <span class="fn">len</span>(seq)
    <span class="kw">for</span> ul <span class="kw">in</span> <span class="fn">range</span>(min_unit, max_unit + <span class="nu">1</span>):
        i = <span class="nu">0</span>
        <span class="kw">while</span> i <= n - ul:
            unit, count, j = seq[i:i+ul], <span class="nu">1</span>, i + ul
            <span class="kw">while</span> j + ul <= n <span class="kw">and</span> seq[j:j+ul] == unit: count += <span class="nu">1</span>; j += ul
            <span class="kw">if</span> count >= min_rep: out.append((i, j, unit, count)); i = j
            <span class="kw">else</span>: i += <span class="nu">1</span>
    <span class="kw">return</span> out

<span class="kw">def</span> <span class="fn">_classify</span>(seq: str, pos: int):
    rr = rc = rp = nr = <span class="st">"No"</span>
    <span class="kw">for</span> s, e, unit, cnt <span class="kw">in</span> <span class="fn">_find_repeats</span>(seq):
        <span class="kw">if</span> s + <span class="nu">1</span> <= pos <= e:
            <span class="kw">return</span> seq[s:e], <span class="fn">str</span>(cnt), <span class="fn">str</span>((pos - s - <span class="nu">1</span>) % <span class="fn">len</span>(unit) + <span class="nu">1</span>), nr
    <span class="kw">for</span> s, e, unit, cnt <span class="kw">in</span> <span class="fn">_find_repeats</span>(seq):
        <span class="kw">if</span> pos == s <span class="kw">or</span> pos == e + <span class="nu">1</span>:
            nr = <span class="st">"Yes"</span>; rr = seq[s:e]; rc = <span class="fn">str</span>(cnt); <span class="kw">break</span>
    <span class="kw">return</span> rr, rc, rp, nr

<span class="kw">def</span> <span class="fn">_repeat_filter</span>(table: Path, mode: str, out: Path, fp: Path, ref: Path):
    hdr = <span class="st">"CHROM\tPOS\tREF\tALT\tExtracted_REF\tRef_seq_marked\tRepeatRegion\tRepeatCount\tREFpos_inRepeatUnit\tNextToRepeat\n"</span>
    <span class="kw">with</span> <span class="fn">open</span>(table) <span class="kw">as</span> fin, <span class="fn">open</span>(out, <span class="st">"w"</span>) <span class="kw">as</span> fo, <span class="fn">open</span>(fp, <span class="st">"w"</span>) <span class="kw">as</span> ff:
        fo.write(hdr); ff.write(hdr)
        col = {}
        <span class="kw">for</span> i, row <span class="kw">in</span> <span class="fn">enumerate</span>(fin):
            r = row.rstrip(<span class="st">"\n"</span>).split(<span class="st">"\t"</span>)
            <span class="kw">if not</span> i: col = {h: j <span class="kw">for</span> j, h <span class="kw">in</span> <span class="fn">enumerate</span>(r)}; <span class="kw">continue</span>
            chrom, pos, ref_a, alt = r[col[<span class="st">"CHROM"</span>]], <span class="fn">int</span>(r[col[<span class="st">"POS"</span>]]), r[col[<span class="st">"REF"</span>]], r[col[<span class="st">"ALT"</span>]]
            st = <span class="fn">max</span>(<span class="nu">1</span>, pos - <span class="nu">100</span>)
            res = subprocess.run([<span class="st">"samtools"</span>, <span class="st">"faidx"</span>, <span class="fn">str</span>(ref), <span class="st">f"{chrom}:{st}-{pos+100}"</span>],
                                 capture_output=<span class="kw">True</span>, text=<span class="kw">True</span>)
            seq = <span class="st">""</span>.join(l <span class="kw">for</span> l <span class="kw">in</span> res.stdout.splitlines() <span class="kw">if not</span> l.startswith(<span class="st">">"</span>))
            <span class="kw">if not</span> seq:
                line = <span class="st">f"{chrom}\t{pos}\t{ref_a}\t{alt}\tNo\tNo\tNo\tNo\tNo\tNo\n"</span>
                fo.write(line); ff.write(line); <span class="kw">continue</span>
            idx = pos - st + <span class="nu">1</span>
            ext = seq[idx-<span class="nu">1</span>] <span class="kw">if</span> idx <= <span class="fn">len</span>(seq) <span class="kw">else</span> <span class="st">"?"</span>
            marked = <span class="st">f"{seq[:idx-1]}[{seq[idx-1:idx]}]{seq[idx:]}"</span>
            rr, rc, rp, nr = <span class="fn">_classify</span>(seq, idx)
            line = <span class="st">f"{chrom}\t{pos}\t{ref_a}\t{alt}\t{ext}\t{marked}\t{rr}\t{rc}\t{rp}\t{nr}\n"</span>
            is_fp = (mode == <span class="st">"SNP"</span> <span class="kw">and</span> rr != <span class="st">"No"</span> <span class="kw">and</span> (rc == <span class="st">"No"</span> <span class="kw">or</span> <span class="fn">int</span>(rc) >= <span class="nu">10</span>)) <span class="kw">or</span> \
                    (mode == <span class="st">"INDEL"</span> <span class="kw">and</span> rr != <span class="st">"No"</span>)
            (ff <span class="kw">if</span> is_fp <span class="kw">else</span> fo).write(line)

<span class="kw">def</span> <span class="fn">_gatk_filter_table</span>(vcf_gz: Path, vtype: str, out_dir: Path, ref: Path):
    base = vcf_gz.name[:-<span class="nu">7</span>]
    sfx  = <span class="st">"snp"</span> <span class="kw">if</span> vtype == <span class="st">"SNP"</span> <span class="kw">else</span> <span class="st">"indels"</span>
    sel  = out_dir / <span class="st">f"{base}_{sfx}.vcf"</span>
    filt = out_dir / <span class="st">f"{base}_{sfx}_filtered.vcf"</span>
    fname = <span class="st">"QD2DP10SOR3FS60MQ50"</span>   <span class="kw">if</span> vtype == <span class="st">"SNP"</span> <span class="kw">else</span> <span class="st">"QD2DP10FS200MQ50"</span>
    fexpr = <span class="st">"QD&lt;2||DP&lt;10||SOR&gt;3||FS&gt;60||MQ&lt;50"</span> <span class="kw">if</span> vtype == <span class="st">"SNP"</span> \
            <span class="kw">else</span> <span class="st">"QD&lt;2||DP&lt;10||FS&gt;200||MQ&lt;50"</span>
    run([<span class="st">"gatk"</span>, <span class="st">"SelectVariants"</span>, <span class="st">"-R"</span>, <span class="fn">str</span>(ref), <span class="st">"-V"</span>, <span class="fn">str</span>(vcf_gz),
         <span class="st">"--select-type-to-include"</span>, vtype, <span class="st">"-O"</span>, <span class="fn">str</span>(sel)], step=<span class="st">f"9b-select-{vtype}"</span>)
    run([<span class="st">"gatk"</span>, <span class="st">"VariantFiltration"</span>, <span class="st">"-R"</span>, <span class="fn">str</span>(ref), <span class="st">"-V"</span>, <span class="fn">str</span>(sel),
         <span class="st">"-O"</span>, <span class="fn">str</span>(filt), <span class="st">"--filter-name"</span>, fname, <span class="st">"--filter-expression"</span>, fexpr],
        step=<span class="st">f"9c-filter-{vtype}"</span>)
    sel.unlink(missing_ok=<span class="kw">True</span>)
    gz = compress_index(filt, step=<span class="st">f"9d-compress-{vtype}"</span>)
    tbl_dir = out_dir / <span class="st">"Table"</span>; tbl_dir.mkdir(exist_ok=<span class="kw">True</span>)
    run([<span class="st">"gatk"</span>, <span class="st">"VariantsToTable"</span>, <span class="st">"-V"</span>, <span class="fn">str</span>(gz),
         <span class="st">"-F"</span>, <span class="st">"CHROM"</span>, <span class="st">"-F"</span>, <span class="st">"POS"</span>, <span class="st">"-F"</span>, <span class="st">"QUAL"</span>, <span class="st">"-F"</span>, <span class="st">"REF"</span>, <span class="st">"-F"</span>, <span class="st">"ALT"</span>,
         <span class="st">"-F"</span>, <span class="st">"TYPE"</span>, <span class="st">"-F"</span>, <span class="st">"FILTER"</span>, <span class="st">"-F"</span>, <span class="st">"FS"</span>, <span class="st">"-F"</span>, <span class="st">"SOR"</span>,
         <span class="st">"-GF"</span>, <span class="st">"AF"</span>, <span class="st">"-GF"</span>, <span class="st">"AD"</span>, <span class="st">"-GF"</span>, <span class="st">"GT"</span>, <span class="st">"-GF"</span>, <span class="st">"GQ"</span>, <span class="st">"-GF"</span>, <span class="st">"SB"</span>,
         <span class="st">"-O"</span>, <span class="fn">str</span>(tbl_dir / gz.name.replace(<span class="st">".vcf.gz"</span>, <span class="st">".table"</span>))],
        step=<span class="st">f"9e-table-{vtype}"</span>)

<span class="kw">def</span> <span class="fn">step9_mutation_filter</span>(cfg) -> <span class="kw">None</span>:
    anc_dir = cfg.variants_dir / <span class="st">"Filtered_against_ancestors"</span>
    snp_dir = cfg.variants_dir / <span class="st">"SNP"</span>
    ind_dir = cfg.variants_dir / <span class="st">"INDELS"</span>
    mkdirs(anc_dir, snp_dir, ind_dir)

    <span class="cm"># 9a — subtract ancestor VCFs (any number supported)</span>
    <span class="kw">for</span> vcf <span class="kw">in</span> <span class="fn">sorted</span>(cfg.vcf_dir.iterdir()):
        <span class="kw">if</span> vcf.suffix == <span class="st">".vcf"</span>: vcf = compress_index(vcf, step=<span class="st">"9-prep"</span>)
        <span class="kw">if not</span> (vcf.suffix == <span class="st">".gz"</span> <span class="kw">and</span> vcf.stem.endswith(<span class="st">".vcf"</span>)): <span class="kw">continue</span>
        current = vcf
        <span class="kw">for</span> j, anc <span class="kw">in</span> <span class="fn">enumerate</span>(cfg.ancestor_vcfs):
            isec = vcf.parent / <span class="st">f"{vcf.stem}_anc{j}_isec"</span>
            run([<span class="st">"bcftools"</span>, <span class="st">"isec"</span>, <span class="st">"-p"</span>, <span class="fn">str</span>(isec), <span class="st">"-Oz"</span>, <span class="fn">str</span>(anc), <span class="fn">str</span>(current)],
                step=<span class="st">f"9a-isec-anc{j}"</span>)
            nxt = anc_dir / <span class="st">f"{vcf.stem}_pass{j}.vcf.gz"</span> <span class="kw">if</span> j < <span class="fn">len</span>(cfg.ancestor_vcfs)-<span class="nu">1</span> \
                  <span class="kw">else</span> anc_dir / <span class="st">f"{vcf.stem}_anc.vcf.gz"</span>
            (isec / <span class="st">"0001.vcf.gz"</span>).rename(nxt)
            compress_index(nxt, step=<span class="st">f"9a-idx-{j}"</span>)
            subprocess.run([<span class="st">"rm"</span>, <span class="st">"-rf"</span>, <span class="fn">str</span>(isec)])
            <span class="kw">if</span> j > <span class="nu">0</span>: current.unlink(missing_ok=<span class="kw">True</span>)
            current = nxt

    <span class="cm"># 9b-9e — GATK filtering + repeat filter</span>
    <span class="kw">for</span> anc_vcf <span class="kw">in</span> <span class="fn">sorted</span>(anc_dir.glob(<span class="st">"*_anc.vcf.gz"</span>)):
        <span class="kw">for</span> vtype, odir <span class="kw">in</span> [(<span class="st">"SNP"</span>, snp_dir), (<span class="st">"INDEL"</span>, ind_dir)]:
            <span class="fn">_gatk_filter_table</span>(anc_vcf, vtype, odir, cfg.ref)
    <span class="kw">for</span> mode, tdir <span class="kw">in</span> [(<span class="st">"SNP"</span>, snp_dir/<span class="st">"Table"</span>), (<span class="st">"INDEL"</span>, ind_dir/<span class="st">"Table"</span>)]:
        <span class="kw">for</span> tbl <span class="kw">in</span> <span class="fn">sorted</span>(tdir.glob(<span class="st">"*filtered.table"</span>)):
            <span class="fn">_repeat_filter</span>(tbl, mode,
                            tbl.with_name(tbl.stem + <span class="st">"_output.tsv"</span>),
                            tbl.with_name(tbl.stem + <span class="st">"_falsepos.tsv"</span>),
                            cfg.ref)

<span class="cm"># ── CLI ─────────────────────────────────────────────────────────────────────</span>
<span class="kw">def</span> <span class="fn">parse_args</span>():
    p = argparse.ArgumentParser(
        description=<span class="st">"End-to-end genomic variant calling pipeline."</span>,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(<span class="st">"--project-dir"</span>,  required=<span class="kw">True</span>, type=Path,
                   help=<span class="st">"Root output directory (created if absent)"</span>)
    p.add_argument(<span class="st">"--ref"</span>,          required=<span class="kw">True</span>, type=Path,
                   help=<span class="st">"Reference genome FASTA (any organism)"</span>)
    p.add_argument(<span class="st">"--ancestor-vcf"</span>, dest=<span class="st">"ancestor_vcfs"</span>, action=<span class="st">"append"</span>,
                   type=Path, default=[],
                   help=<span class="st">"Ancestor VCF(s) to subtract. Repeat flag for multiple."</span>)
    p.add_argument(<span class="st">"--ploidy"</span>,     type=<span class="fn">int</span>, default=<span class="nu">2</span>)
    p.add_argument(<span class="st">"--threads"</span>,    type=<span class="fn">int</span>, default=<span class="nu">8</span>)
    p.add_argument(<span class="st">"--skip-index"</span>, action=<span class="st">"store_true"</span>)
    p.add_argument(<span class="st">"--start-step"</span>, type=<span class="fn">int</span>, default=<span class="nu">1</span>, choices=<span class="fn">range</span>(<span class="nu">1</span>,<span class="nu">10</span>))
    <span class="cm"># Trimmomatic knobs</span>
    p.add_argument(<span class="st">"--trim-leading"</span>,  type=<span class="fn">int</span>, default=<span class="nu">3</span>)
    p.add_argument(<span class="st">"--trim-trailing"</span>, type=<span class="fn">int</span>, default=<span class="nu">3</span>)
    p.add_argument(<span class="st">"--trim-window"</span>,   type=<span class="fn">int</span>, default=<span class="nu">4</span>)
    p.add_argument(<span class="st">"--trim-quality"</span>,  type=<span class="fn">int</span>, default=<span class="nu">20</span>)
    p.add_argument(<span class="st">"--trim-minlen"</span>,   type=<span class="fn">int</span>, default=<span class="nu">36</span>)
    p.add_argument(<span class="st">"--trim-headcrop"</span>, type=<span class="fn">int</span>, default=<span class="nu">15</span>)
    p.add_argument(<span class="st">"--trim-crop"</span>,     type=<span class="fn">int</span>, default=<span class="nu">150</span>)
    <span class="kw">return</span> p.parse_args()

<span class="kw">def</span> <span class="fn">build_config</span>(args):
    <span class="st">"""Derive all directory paths from --project-dir."""</span>
    d = args.project_dir
    args.raw_dir         = d / <span class="st">"Raw"</span>
    args.trimmed_paired  = d / <span class="st">"Trimmomatic/Paired"</span>
    args.trimmed_unpaired= d / <span class="st">"Trimmomatic/Unpaired"</span>
    args.aligned_dir     = d / <span class="st">"1.Aligned"</span>
    args.sorted_dir      = d / <span class="st">"2.Sorted"</span>
    args.marked_dir      = d / <span class="st">"3.Marked_duplicates"</span>
    args.fixed_rg_dir    = d / <span class="st">"4.Fixed_read_group"</span>
    args.vcf_dir         = d / <span class="st">"VCF_add_annotations"</span>
    args.variants_dir    = d / <span class="st">"variants_call"</span>
    <span class="kw">return</span> args

<span class="kw">def</span> <span class="fn">main</span>():
    args = <span class="fn">parse_args</span>()
    cfg  = <span class="fn">build_config</span>(args)
    setup_logging(cfg.project_dir / <span class="st">"pipeline.log"</span>)
    mkdirs(cfg.project_dir)

    steps = {
        <span class="nu">1</span>: step1_trimmomatic,   <span class="nu">2</span>: step2_index_reference,
        <span class="nu">3</span>: step3_align_and_sort, <span class="nu">4</span>: step4_index_bam,
        <span class="nu">5</span>: step5_mark_duplicates,<span class="nu">6</span>: step6_fix_read_groups,
        <span class="nu">7</span>: step7_index_fixed_bams,<span class="nu">8</span>: step8_call_variants,
        <span class="nu">9</span>: step9_mutation_filter,
    }
    <span class="kw">for</span> n <span class="kw">in</span> <span class="fn">range</span>(cfg.start_step, <span class="nu">10</span>):
        <span class="kw">if</span> n == <span class="nu">2</span> <span class="kw">and</span> cfg.skip_index:
            log.info(<span class="st">"Step 2 skipped (--skip-index)."</span>); <span class="kw">continue</span>
        log.info(<span class="st">f"── Starting step {n} ──"</span>)
        steps[n](cfg)
    log.info(<span class="st">"Pipeline complete."</span>)

<span class="kw">if</span> __name__ == <span class="st">"__main__"</span>:
    <span class="fn">main</span>()</pre>
  </div>

  <!-- ── USAGE ── -->
  <div id="usage" class="section-head">
    <h2>Usage &amp; configuration</h2>
    <span class="section-tag">cli reference</span>
  </div>

  <div class="usage-grid">
    <div class="usage-card">
      <h4>Diploid organism, single ancestor</h4>
      <code>python genomic_variant_pipeline.py \
  --project-dir /data/my_project \
  --ref /refs/genome.fa \
  --ancestor-vcf /refs/ancestor.vcf.gz \
  --ploidy 2 \
  --threads 16</code>
      <p class="note">Place paired FASTQ files in <code style="font-family:var(--font-mono);font-size:11px">my_project/Raw/</code> before running. All intermediate directories are created automatically.</p>
    </div>
    <div class="usage-card">
      <h4>Tetraploid, multiple ancestors, resume from step 5</h4>
      <code>python genomic_variant_pipeline.py \
  --project-dir /data/gob8_project \
  --ref /refs/gob8_reference_v1.fa \
  --ancestor-vcf /refs/PM_t0.vcf.gz \
  --ancestor-vcf /refs/PA_t0.vcf.gz \
  --ploidy 4 \
  --threads 20 \
  --skip-index \
  --start-step 5</code>
      <p class="note">Multiple <code style="font-family:var(--font-mono);font-size:11px">--ancestor-vcf</code> flags chain successive bcftools isec passes. <code style="font-family:var(--font-mono);font-size:11px">--skip-index</code> skips BWA indexing if already done.</p>
    </div>
    <div class="usage-card">
      <h4>All CLI flags</h4>
      <code>--project-dir    Root directory (required)
--ref            Reference FASTA (required)
--ancestor-vcf   Ancestor VCF(s); repeat for multiple
--ploidy         Organism ploidy (default: 2)
--threads        CPU threads (default: 8)
--skip-index     Skip BWA index (step 2)
--start-step     Resume from step 1–9 (default: 1)
--trim-leading   Trimmomatic LEADING (default: 3)
--trim-trailing  Trimmomatic TRAILING (default: 3)
--trim-window    Sliding window size (default: 4)
--trim-quality   Sliding window quality (default: 20)
--trim-minlen    Minimum read length (default: 36)
--trim-headcrop  Bases to crop from head (default: 15)
--trim-crop      Max read length after crop (default: 150)</code>
    </div>
    <div class="usage-card">
      <h4>Output structure</h4>
      <code>project-dir/
├── Raw/                  ← input FASTQ files here
├── Trimmomatic/
├── 1.Aligned/
├── 2.Sorted/
├── 3.Marked_duplicates/
├── 4.Fixed_read_group/
├── VCF_add_annotations/
├── variants_call/
│   ├── Filtered_against_ancestors/
│   ├── SNP/Table/        ← *_output.tsv
│   └── INDELS/Table/     ← *_output.tsv
└── pipeline.log</code>
    </div>
  </div>

</main>

<footer>
  variant-pipeline · Python · GATK · BWA · Picard · bcftools
</footer>

<script>
function copyCode() {
  const el = document.getElementById('code-block');
  const text = el.innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1800);
  });
}
</script>
</body>
</html>
