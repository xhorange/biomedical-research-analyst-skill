# biomedical-research-analyst

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://www.anthropic.com/claude)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

A [Claude Skill](https://www.anthropic.com/news/skills) for conducting
rigorous, source-verifiable biomedical research analyses and producing
publication-style slide decks. The skill formalizes a disciplined analytical
workflow — dataset verification, statistically appropriate methodology,
explicit separation of data-derived and literature-derived evidence, and a
mandatory post-hoc fact-checking pass — as a reusable specification that a
language model can follow consistently across studies.

[中文说明](README.zh-CN.md)

## Overview

Large language models can readily produce biomedical analysis deliverables
that are fluent, well-formatted, and superficially authoritative — complete
with gene identifiers, statistical values, figures, and a references section.
The correctness of such output, however, is not guaranteed by its
presentation quality. In the absence of an explicit verification discipline,
several failure modes recur:

1. **Dataset misattribution.** A dataset is used on the strength of its
   filename or accession number without confirming, from the primary record,
   that it corresponds to the condition under study.
2. **Evidentiary conflation.** Claims drawn from the literature are presented
   indistinguishably from findings produced by the analysis itself, without
   a traceable citation.
3. **Unverified pathway–gene attribution.** A gene is described as belonging
   to a given biological pathway on the basis of general domain knowledge
   rather than the specific overlap reported by the enrichment analysis,
   which can misassign a genuinely significant result to an incorrect
   pathway.
4. **Overstatement of inferential strength.** Associative language is
   replaced with causal or confirmatory language ("proves," "confirms") that
   the underlying study design — frequently cross-sectional or
   observational — does not support.

This skill was formulated after each of the above failure modes was observed,
identified, and corrected during an applied analysis (documented in
[Illustrative application](#illustrative-application)). Rather than relying on
these corrections being independently rediscovered in each subsequent
analysis, the skill encodes them as a standing methodological requirement.

## Repository layout

```
biomedical-research-analyst/
├── SKILL.md                          # trigger conditions, the analytical workflow, and a pre-delivery checklist
├── references/
│   ├── dataset_verification.md       # procedure for confirming a public dataset matches the research question
│   ├── statistical_methods.md        # method selection by data type, threshold pre-registration, enrichment caveats
│   ├── fact_check_checklist.md       # the mandatory re-verification procedure, documented against an observed failure
│   └── ppt_structure.md              # slide organization, citation format, and structural validation of the deck
└── scripts/
    ├── parse_geo_series_matrix.py    # GEO series matrix parser (no GEOparse dependency)
    ├── differential_expression.py    # Welch's t-test with Benjamini-Hochberg FDR correction, two-group comparison
    └── pptx_helpers.py               # reusable python-pptx components (title bars, tables, proportionate image placement)
```

`SKILL.md` constitutes the primary specification consulted by the model.
Files under `references/` are loaded on demand at the relevant step of the
workflow rather than held in context at all times. The scripts under
`scripts/` are intended as adaptable components rather than a fixed pipeline,
as dataset metadata conventions vary across sources.

## Methodology

The skill specifies the following sequence of analytical stages:

| Stage | Objective |
|---|---|
| 0 | Classify the research question (comparative, single-mechanism, or risk-factor synthesis) to determine the applicable strategy. |
| 1 | Verify any dataset against its primary record — title, abstract, sample grouping, and platform — prior to use. |
| 2 | Determine the evidentiary strategy: proceed with public data where a genuine match exists, or state explicitly that the analysis is literature-based where it does not. |
| 3 | Execute the analysis using a method appropriate to the data type, with thresholds specified prior to inspection of results and all intermediate outputs persisted to disk. |
| 4 | Integrate literature evidence with verifiable citations (author, journal, year, PMID), maintained as distinct from data-derived findings. |
| 5 | Assess concordance between analytical findings and established biological knowledge as an internal consistency check. |
| 6 | Perform a mandatory fact-check pass: re-verify every specific claim — pathway–gene attribution, summary statistics, significance thresholds — against the underlying result files, and audit inferential language against the study design. |
| 7 | Report limitations, including confounds that are not immediately apparent (e.g., whether an observed shared signature reflects a feature specific to the conditions compared, or a generic characteristic of a broader disease class). |
| 8 | Assemble the deliverable and validate its structure programmatically (slide count, embedded figures and tables) prior to delivery. |

The rationale underlying each stage, including the observed failure that
motivated it, is documented in `SKILL.md` and the corresponding files under
`references/`.

## Installation

**Claude Code:**
```bash
mkdir -p ~/.claude/skills
cp -r biomedical-research-analyst ~/.claude/skills/
```
Upon starting a new session, the skill becomes available for invocation;
Claude determines applicability based on the `description` field in the
`SKILL.md` frontmatter.

**Claude.ai:** upload the directory (or an equivalent packaged `.skill`
archive) to a workspace supporting custom skills.

## Dependencies

The bundled scripts require a Python environment providing:

```
pandas
numpy
scipy
statsmodels
gseapy       # Enrichr-based functional enrichment analysis
python-pptx  # slide deck construction
matplotlib   # figure generation (volcano plots, Venn diagrams, bar charts)
Pillow       # required by pptx_helpers.add_pic_fit
```

Missing packages are installed as required at runtime; this list is provided
for reference.

## Illustrative application

The skill was derived from an analysis investigating shared molecular risk
factors between **rheumatoid arthritis** and **atherosclerosis**, using two
independent GEO datasets (GSE55235, synovial tissue; GSE100927, arterial
tissue). Excluding data acquisition — which is network-dependent and subject
to variable latency — the analytical pipeline (parsing, differential
expression analysis, set intersection, functional enrichment, and assembly of
a twelve-slide deck) completes in approximately ten minutes.

The fact-checking stage identified two inaccuracies prior to delivery:

- A set of chemokine receptor genes (CCR1, CCR2, CCR5, CCR7) had been
  attributed, in a summary diagram, to the "leukocyte transendothelial
  migration" pathway. Examination of the underlying Enrichr output indicated
  that these genes constituted the significant overlap for a distinct term
  ("chemokine signaling pathway"), whereas the transendothelial migration
  term's overlap was attributable to CXCR4, ITGAL, and MMP9.
- A claim describing "macrophage/foam-cell-like activation" was found to be
  partially unsupported: macrophage activation reached statistical
  significance, whereas the foam-cell differentiation term did not
  (adjusted P ≈ 0.25–0.34).

Both inaccuracies were identified by cross-referencing each specific claim
against the corresponding result file — the procedure specified as mandatory
in `references/fact_check_checklist.md`.

## Scope and limitations

This skill governs the analytical *process* — verification, methodological
appropriateness, and evidentiary traceability. It does not substitute for
domain expertise in study interpretation, and outputs produced under this
skill remain hypothesis-generating unless the underlying data and design
support a stronger inferential claim, which the skill's own limitations
stage is designed to make explicit.

## Contributing

Contributions are welcome, particularly reports of observed failure modes.
See [CONTRIBUTING.md](CONTRIBUTING.md) for what makes a useful report or
pull request.

## License

Released under the MIT License; see [LICENSE](LICENSE).
