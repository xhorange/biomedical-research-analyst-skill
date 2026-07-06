# Statistical methods

## Match the method to the data type

**Microarray intensity data** (Affymetrix MAS5, Agilent Feature Extraction,
etc.) is continuous and roughly log-normal once log-transformed. Welch's
t-test per gene (unequal variance, doesn't assume equal group sizes) followed
by Benjamini-Hochberg FDR correction across all tested genes is a standard,
defensible approach. `scripts/differential_expression.py` implements this.

Check whether the series matrix values are already log-scale or linear-scale
before running anything — this is stated (sometimes obliquely) in
`!Series_data_processing` in the series matrix header. Linear-scale MAS5
intensities need `log2(clip(x, lower=1))` before t-tests / fold-change
calculations; already-log-scale processed signal (common for newer
Agilent/Illumina pipelines) should not be log-transformed again. Getting this
wrong silently produces fold-changes that are off by orders of magnitude
while still "looking like a fold change," so always print the raw value range
before deciding.

**RNA-seq count data** is NOT the same as microarray intensities — raw or
even normalized counts are discrete, over-dispersed, and mean-variance
dependent. Running a t-test directly on counts (or even on naively
log-transformed counts) will misestimate significance, especially for
low-count genes. If a dataset provides raw or lightly-normalized counts, the
statistically appropriate approach is a count-aware model (e.g., a
DESeq2-style negative-binomial GLM, or edgeR/limma-voom). Doing this properly
in Python typically means using `pydeseq2` if available, or falling back to
CPM-normalization + log-transform + a t-test as an explicitly-labeled
approximation (state that it's an approximation, don't present it as
equivalent to a proper count model). Never reuse the microarray Welch's-test
script on raw RNA-seq counts and call it the same method.

## Multi-probe / multi-transcript collapsing

When a platform has multiple probes per gene, decide a deterministic
tie-breaking rule up front and document it (e.g., "keep the probe with the
largest absolute log2FC" — used in this skill's bundled scripts). Don't
average probes with wildly different signal unless you've checked that's
sensible for the platform.

## Threshold discipline

Decide the significance threshold (e.g., `|log2FC| >= 1` and `FDR < 0.05`)
*before* seeing how many genes pass it, and use the same threshold across
every comparison in the analysis. If a threshold produces very few hits (e.g.,
a small-n comparison yields almost nothing at FDR < 0.05), it is fine to
report that honestly and note it as a power limitation — it is not fine to
quietly loosen the threshold until a "reasonable-looking" number of hits
appears, without disclosing that the threshold changed and why.

## Multiple testing correction

Always correct for multiple comparisons across the full set of genes tested
in that comparison (Benjamini-Hochberg FDR is standard and implemented in
`statsmodels.stats.multitest.multipletests`). Report raw p-values alongside
FDR-adjusted values in saved output tables so a reviewer can see both.

## Functional enrichment

When running enrichment (e.g., via `gseapy.enrichr`), record which gene-set
library and version was used (e.g., "GO_Biological_Process_2023",
"KEGG_2021_Human") since Enrichr's underlying libraries are periodically
updated and results are not guaranteed to reproduce exactly against a future
library version. Use the adjusted p-value column for significance claims, not
the raw p-value.

**Critical: after enrichment, do not assume which of your input genes belong
to which returned term.** Enrichr's output includes a `Genes` column per term
listing exactly which of your input genes overlapped that specific term. When
describing a pathway in prose or a diagram, read that gene list for that
specific row — a gene can be significantly enriched overall while belonging to
a *different* pathway than the one you assumed, because it appears in
multiple gene sets. This exact mistake (attributing a set of chemokine
receptor genes to "leukocyte transendothelial migration" when Enrichr's own
output showed they were actually the overlap for "chemokine signaling
pathway") is what motivated the mandatory fact-check pass in this skill — see
`fact_check_checklist.md`.
