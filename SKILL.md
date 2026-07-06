---
name: biomedical-research-analyst
description: Use this skill whenever the user asks for a rigorous, evidence-backed analysis of a biomedical, clinical, or life-sciences research question that should end in a clear conclusion plus a slide deck (PPT) — e.g. comparing molecular mechanisms between two diseases, investigating a gene/pathway/biomarker's role in a condition, evaluating shared or novel risk factors, or synthesizing evidence around a drug mechanism. Trigger this proactively whenever a request combines a biomedical/medical/genomics topic with wanting a report, deck, PPT, 汇报, 分析报告, or "give me the conclusion" — even if the user never says "skill", never spells out the steps, or only hands over a rough dataset file / GEO accession / gene list. This skill's dataset-verification and mandatory fact-check steps exist specifically to catch confidently-written but wrong, mismatched, or fabricated biomedical claims before they reach the user, so invoke it whenever sourcing and accuracy matter — not for casual trivia questions about biology.
---

# Biomedical Research Analyst

## Why this skill exists

Biomedical analysis is one of the few domains where a fluent, well-formatted, wrong
answer is worse than no answer — someone may use it to guide real research
direction or clinical thinking. The failure modes are specific and recurring:
a dataset that sounds right (by name or accession) but covers the wrong disease;
a literature claim dressed up as this analysis's own finding; a pathway-gene
attribution written from memory instead of the actual output file; a threshold
quietly loosened until the "right" number of hits appears; a confident causal
claim built on cross-sectional data. None of these require malice — they happen
because generating a compelling narrative is easier than checking it. This
skill exists to force the checking.

The standard this skill holds to: every specific number, gene, pathway, or
percentage anyone could double-click on in the final deliverable must trace
back to either (a) a saved intermediate file this session produced, or (b) a
cited paper you actually looked up. If it doesn't trace back to one of those
two things, it doesn't go in the deck.

## Step 0: Understand what's actually being asked

Biomedical questions vary a lot in shape — read carefully before picking a
strategy:

- **Comparative** ("do RA and atherosclerosis share risk factors?", "how does
  gene X's role differ in cancer A vs cancer B?") — usually wants a shared
  vs. distinct mechanism analysis across two or more conditions.
- **Single-topic mechanism** ("what does gene X do in disease Y?", "how does
  drug Z work?") — usually wants a synthesis of the mechanism, evidence
  strength, and open questions, possibly anchored by one dataset rather than
  an intersection of several.
- **Risk-factor / epidemiology style** ("what increases risk of Y?") — often
  literature-only; there may be no single dataset that directly answers it.

If the user supplies a file, path, or accession number, do not assume it is
what its name claims. Read `references/dataset_verification.md` before
touching it — the case that motivated this skill was a user-provided file
named after a rheumatoid-arthritis-sounding study that turned out, on actual
inspection, to be colorectal cancer liver metastasis data. Catching that before
running any analysis, not after, is the entire point of this step.

## Step 1: Decide the data strategy

Ask yourself: is there public data that could actually speak to this question,
and can it realistically be obtained in this session?

- **Yes, and it's comparative/omics-shaped** → search GEO (or another
  appropriate public repository — ArrayExpress, TCGA, etc.) for datasets
  whose title, summary, tissue, and sample grouping genuinely match the
  question. Confirm this from the repository page itself, not from the
  accession number looking plausible. See `references/dataset_verification.md`
  for the checklist and for handling flaky downloads (NCBI FTP in particular
  is often slow in sandboxed environments — use resumable `curl -C -`,
  retries, and background tasks rather than assuming one shot will work).
- **No suitable dataset exists, or it can't be downloaded/parsed in a
  reasonable time** → say so plainly and fall back to a literature-only
  synthesis. A well-sourced literature review beats a data analysis built on
  a dataset that doesn't really fit. Never substitute a "close enough"
  dataset without flagging the mismatch explicitly to the user and in the
  deliverable.
- **Question doesn't need data at all** (pure mechanism/pathway question with
  strong existing consensus) → literature synthesis is the whole job; skip to
  Step 3.

## Step 2: Run the analysis (when using omics data)

Read `references/statistical_methods.md` before writing analysis code — it
covers the difference between microarray intensity data (Welch's t-test +
Benjamini-Hochberg FDR, the pattern used in this skill's bundled scripts) and
RNA-seq count data (which needs count-aware modeling, not a t-test on raw
counts), plus the rule about locking in significance thresholds *before*
looking at how many hits they produce.

Bundled scripts (adapt, don't necessarily use verbatim — every dataset's
metadata format differs):

- `scripts/parse_geo_series_matrix.py` — parses a GEO series matrix file
  (expression table + `!Sample_characteristics_ch1` metadata) into a
  DataFrame pair, without needing GEOparse.
- `scripts/differential_expression.py` — Welch's t-test + BH-FDR helper for
  two-group comparison on already-log-scaled expression data.

General shape of the pipeline for a comparative question:
1. Parse expression matrix + sample metadata for each dataset.
2. Map probes/features to gene symbols using the correct platform annotation
   file (check what a probe actually maps to — multi-mapping probes need a
   documented tie-breaking rule, e.g. "keep the probe with largest |log2FC|").
3. Compute per-gene differential expression per dataset, with the
   pre-registered threshold (e.g. |log2FC| ≥ 1, FDR < 0.05) applied uniformly.
4. For multi-condition comparisons: intersect gene sets, classify
   concordant/discordant direction changes, run functional enrichment (e.g.
   Enrichr via `gseapy`) on the biologically interesting subset (usually
   concordant-direction genes), and note exactly which gene-set library
   version was used since results shift as libraries update.
5. Save every intermediate table (raw fold-changes, per-dataset DEG lists,
   intersections, enrichment results) to disk as CSV. If a number appears in
   the final deck, a reviewer should be able to open a file and find it.

## Step 3: Literature integration

Anything not derived from this session's own data analysis needs an explicit
source: author, journal, year, and PMID where findable. Actually look these
papers up (WebSearch/WebFetch) rather than relying on trained-in recall —
specific numbers, effect sizes, and PMIDs are exactly the kind of detail
models misremember with confidence. If you can't verify a specific claim,
soften it to what you can verify, or drop it.

Keep data-driven and literature-driven content visibly separate in the
deliverable — different slides/sections, explicit "来自本次分析" vs "文献报道"
labeling. Never let a literature-derived claim get described as something
"this analysis found," and never let a real data finding go uncredited to the
dataset it came from.

## Step 4: Internal consistency check

Before drafting conclusions, check whether the analysis surfaced genes,
pathways, or effects already well known in the literature for this topic
(e.g., does a shared-inflammation analysis actually pick up genes like TNF,
IL6, VCAM1, MMP9 that are already reported RA-atherosclerosis crossover
genes?). Partial overlap is expected and fine to report as-is. But if the
result set has *no* connection to anything in the known literature, that's a
signal to re-check the code and thresholds before writing it up — not a
result to explain away with a confident-sounding paragraph.

## Step 5: Mandatory fact-check pass — do this before showing the user anything

This is the step that is easiest to skip and the one most worth never
skipping. Read `references/fact_check_checklist.md` for the full procedure;
the short version:

After drafting the conclusion and any diagram/summary that names specific
genes, pathways, percentages, or significance claims, go back through every
one of them and verify it against the actual saved result file — not against
what you remember writing the analysis to do. Concretely: if a diagram says
"pathway X contains genes A/B/C," grep the enrichment output's gene-overlap
column for that exact pathway term and confirm A/B/C are actually listed
there (they may instead belong to a different, also-significant pathway —
recheck the assignment, don't just recheck significance). Recompute headline
counts straight from the CSV rather than trusting a number typed earlier in
the conversation. Hunt specifically for language that overclaims relative to
the study design — "proves," "confirms," "independently validates" — cross-
sectional/observational data supports association language, not causal
language.

Do this proactively, as a standard step of finishing the deliverable. Waiting
for the user to ask "is this accurate?" means the wrong version was the one
presented as final.

## Step 6: Limitations — always, and go beyond boilerplate

Every deliverable needs a limitations section, and it needs to do real work,
not recite "small sample size, correlation ≠ causation" and stop there. Think
about what's specifically confound-able in *this* analysis:

- Tissue/platform/species differences between datasets being compared.
- Whether a "shared" signature could just be a generic feature of a broader
  disease class (e.g., any chronic inflammatory disease, any solid tumor, any
  acute infection) rather than something specific to the two conditions in
  question — this is easy to miss because the result still "looks" correct
  and biologically plausible.
- Whether literature-side risk factors (behavioral, genetic) were ever
  actually measured in the datasets used, or are being connected purely by
  narrative.
- Sample size, cross-sectional vs. longitudinal design, and what that does
  and doesn't let you conclude.

## Step 7: Build the PPT

Read `references/ppt_structure.md` for the slide skeleton and citation
formatting conventions. Use `scripts/pptx_helpers.py` for the repeated
plumbing (title bars, tables, bullet lists, image-fit-to-box, background
rectangles) so each new deck doesn't reinvent `python-pptx` boilerplate.

Before calling the deliverable done, read the `.pptx` back with
`python-pptx` and check slide count and that expected images/tables actually
embedded — an assembly bug that silently drops a figure is much cheaper to
catch this way than to have the user discover it.

## Output checklist before you say "done"

- [ ] Every dataset used was verified to actually match the topic (Step 0/1).
- [ ] Every intermediate result (DEG tables, intersections, enrichment
      output) is saved to disk, not just summarized in prose.
- [ ] Every literature claim has a real, checked citation (author/journal/
      year/PMID); no literature claim is presented as this session's finding.
- [ ] The mandatory fact-check pass (Step 5) has actually happened — pathway-
      gene attributions and headline numbers were re-verified against files,
      not recalled from memory.
- [ ] Limitations section names at least one non-obvious confound specific to
      this analysis, not just generic boilerplate.
- [ ] The PPT was read back with python-pptx and its structure verified.
