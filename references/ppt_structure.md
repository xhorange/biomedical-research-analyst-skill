# PPT structure and citation conventions

## Standard skeleton for a comparative (two+ conditions) analysis

Adapt slide count/order to the question, but this order covers the
transparency requirements this skill cares about:

1. **Title** — question/topic, one-line scope, date.
2. **Background & motivation** — why this question matters clinically/
   biologically, cited to literature.
3. **Data & methods** — datasets used (accession, tissue, platform, sample
   sizes) in a table; analysis pipeline steps; and — importantly — a visible
   note of any dataset correction/substitution that happened during the
   session (e.g., "user-provided file X was verified to not match the topic
   and was replaced with Y/Z after re-searching GEO"). Don't bury this in
   silence; it's exactly the kind of thing a careful reviewer would want
   flagged, not discovered.
4. **Per-condition results** — one slide per condition/dataset: key plot
   (e.g., volcano plot) + top-hits table pulled live from the saved results
   file.
5. **Intersection / shared findings** — Venn-style figure + table of the
   shared/concordant items, again pulled from a saved CSV, not hand-typed.
6. **Functional enrichment** (if applicable) — bar chart(s) of top enriched
   terms, labeled with which gene-set library/version was used.
7. **Literature-derived context** — behavioral/genetic/other risk factors or
   mechanisms reported in the literature, NOT from this session's own data.
   Every bullet here should be traceable to an author/journal/year/PMID,
   listed either inline or on the references slide. Make the "this is
   literature, not our data" framing visible in the slide title/subtitle
   itself, not just in a footnote.
8. **Integration** — a diagram or narrative tying the data-driven findings
   (column/section 4-6) to the literature-derived context (column/section 7).
   Caption it honestly: connections drawn between the two sides are
   conceptual/hypothesis-generating unless the same session's data actually
   demonstrated the link.
9. **Limitations** — see SKILL.md Step 6; must include at least one
   non-generic, analysis-specific confound.
10. **Conclusion** — plain-language synthesis. State what's supported and to
    what degree (association vs. mechanism vs. causal), not just what was
    found.
11. **References** — every literature citation used anywhere in the deck,
    with PMID where available, plus a data-sources sub-list (accessions,
    tools/libraries used for analysis, e.g. "Enrichr / gseapy — GO
    Biological Process 2023, KEGG 2021 Human").

For single-topic mechanism questions (no comparative dataset), slides 4-6
collapse into a single "evidence synthesis" section, but sections 2, 3
(methods/sourcing), 9 (limitations), 10 (conclusion), and 11 (references)
still apply.

## Citation formatting

Inline in bullets: `Author et al., Journal, Year, PMID NNNNNNNN.` Keep it
short enough to read on a slide; put full details only on the references
slide if space is tight. Always include the PMID when the paper has one —
it's the cheapest way for a reader to verify the claim themselves, which is
the whole point of citing in the first place.

## Structural validation

After building the `.pptx`, read it back with `python-pptx` before calling
the work done:

```python
from pptx import Presentation
prs = Presentation("output.pptx")
for i, slide in enumerate(prs.slides, 1):
    n_pics = sum(1 for sh in slide.shapes if sh.shape_type == 13)
    n_tables = sum(1 for sh in slide.shapes if sh.has_table)
    print(i, "pics=", n_pics, "tables=", n_tables)
```

Confirm the slide count matches what was intended and that slides expected to
carry a figure/table actually have one embedded — a path typo or a swallowed
exception in the build script can silently produce a slide with a title and
nothing else.

## Reusable building blocks

`scripts/pptx_helpers.py` has ready-to-import helpers for the boilerplate
that shows up in every deck of this kind: colored title bars, image-fit-into-
box placement (preserves aspect ratio), styled tables, and bullet lists.
Import from it rather than re-deriving `python-pptx` shape/textframe code
each time.
