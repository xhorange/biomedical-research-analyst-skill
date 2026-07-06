# Mandatory fact-check pass

## What happened without it

A deck once stated a shared-inflammation diagram claim: "leukocyte
transendothelial migration (CCR1/CCR2/CCR5/CCR7, CXCR4, ITGAL)." It sounded
right — those genes are all real, all significant, all migration-related in a
loose sense. But when the underlying Enrichr output was actually re-opened and
the `Genes` column for the "Leukocyte transendothelial migration" row was
read, only CXCR4/ITGAL/MMP9 were listed there. CCR1/2/5/7 were significant,
but under a *different* row — "Chemokine signaling pathway" / "Cytokine-
cytokine receptor interaction." Both claims were about real, significant
findings; one had the wrong label. The user caught it by asking "is the
conclusion faithful?" — this checklist exists so that question gets asked
and answered before the user ever has to ask it.

A second issue caught in the same pass: a diagram described "macrophage /
foam-cell-like activation" as a finding. Macrophage activation was indeed
significant (adjusted P ≈ 2e-6). Foam cell differentiation specifically was
*not* significant (adjusted P ≈ 0.25–0.34) — it had been included by
plausible-sounding association rather than by checking the actual row.

Both are the same failure mode: writing what sounds right from domain
knowledge instead of reading the file that has the actual answer.

## The procedure

Do this after drafting the conclusion, any integration diagram, and any slide
that names specific genes/pathways/numbers — before presenting the
deliverable as finished.

1. **List every specific factual claim** in the draft: pathway names paired
   with genes, headline counts (e.g., "N shared genes"), significance
   descriptors ("significantly enriched," "the top hit"), and any percentage
   or fold-change quoted directly.
2. **For each pathway-gene pairing**, open the actual enrichment output file
   and find that exact term's row. Read its gene-overlap column and confirm
   every gene you named is actually listed there — not just that the gene is
   *somewhere* in the enrichment results. If a gene isn't in that row, find
   which row it actually belongs to (a `grep`/pandas filter across all rows
   for that gene symbol works well) and either move it to the correct pathway
   label or drop the specific attribution.
3. **For each headline count**, recompute it directly from the saved CSV
   (`len(df)`, a `value_counts()`, a threshold filter) rather than trusting a
   number that was typed into the deck earlier in the session — numbers typed
   from memory drift from the file, especially across multiple edits.
4. **For each significance claim**, check the actual adjusted p-value /ext
   FDR column against the threshold you're citing. "Significantly enriched"
   should mean the row you're citing actually clears the stated threshold —
   not that something adjacent or thematically related did.
5. **Scan for overclaiming language** relative to the actual study design:
   words like "proves," "confirms," "demonstrates causally," "independently
   validates" need cross-sectional/observational data to actually be a
   controlled or longitudinal design to be earned. If the design is
   cross-sectional/observational, the honest verbs are "is consistent with,"
   "supports," "is associated with."
6. **Actively look for the confound you'd be embarrassed to have missed** —
   usually some version of "is this finding specific to what I'm comparing,
   or would it show up in any superficially similar comparison?" (see the
   "generic inflammation signature" example in the main SKILL.md limitations
   section). If you can articulate a plausible alternative explanation for a
   headline finding, put it in the limitations section rather than leaving it
   for the user to think of.

## A quick way to do step 2 at scale

If you have gene symbols of interest and an Enrichr-style results CSV with a
`Genes` column (semicolon-separated), a fast correctness check is:

```python
import pandas as pd
df = pd.read_csv("results/enrich_GO_BP.csv")  # or KEGG, etc.
genes_of_interest = {"CCR1", "CCR2", "CCR5", "CCR7"}
for _, row in df.iterrows():
    overlap = set(row["Genes"].split(";"))
    hit = overlap & genes_of_interest
    if hit:
        print(row["Term"], row["Adjusted P-value"], hit)
```

This prints every term that actually contains each gene of interest, sorted
implicitly by the order Enrichr returned them (usually significance order) —
read this output before writing which pathway a gene "belongs to."
