# Dataset verification

## Why this matters

The incident that motivated this skill: a user handed over
`GSE221608_processed_data.xlsx`, described (by the user, going off the
filename/context) as rheumatoid-arthritis-related expression data. On actual
inspection of the GEO record, GSE221608 turned out to be a 208-sample
colorectal-cancer liver-metastasis mRNA dataset from an unrelated study. Had
the analysis proceeded on the assumption the filename was accurate, every
downstream number would have been a confident, well-formatted description of
the wrong disease. The fix cost nothing except pausing to look.

Filenames, accession numbers, and even what the user believes about a file are
not verification. Verification is opening the source record.

## Checklist before using any dataset

1. **Pull the actual repository record.** For GEO, fetch the GSE summary page
   or `!Series_summary` / `!Series_title` lines from the series matrix header
   — read what the study is actually about, not just its accession number.
2. **Check sample grouping matches the question.** Look at
   `!Sample_characteristics_ch1` (or equivalent) — does it actually split
   samples into the groups you need (disease vs. control, tissue A vs. B)? A
   dataset can be topically related but not have the comparison you need
   (e.g., it has RA samples but no healthy controls).
3. **Check tissue/species/platform.** Confirm the tissue matches what the
   research question is about (synovium vs. whole blood vs. skin are not
   interchangeable for "rheumatoid arthritis" claims), and note the platform
   (microarray chip / RNA-seq) since it determines the analysis method (see
   `statistical_methods.md`).
4. **Check it's actually downloadable in this session.** Public repositories
   (especially NCBI FTP) can be slow or flaky in sandboxed environments.
   Before committing to a dataset in a plan, do a quick connectivity check
   (e.g., `curl -I` on the target URL) rather than discovering the problem
   mid-analysis. For large downloads, use resumable transfer
   (`curl -C - -o file.gz URL`), retry on failure, and consider running the
   download as a background task so a slow connection doesn't block everything
   else.
5. **If the user supplied the file/accession**, still do steps 1-3 yourself.
   Report back what you found, especially if it disagrees with what the user
   believed the file was — that discrepancy is important information for
   them, not an error to silently route around.

## If nothing suitable exists

Don't stretch a mismatched or marginal dataset to fit the question just to
have "real data analysis" in the deliverable. A clearly-labeled
literature-only synthesis is more useful and more honest than a data section
built on a shaky foundation. If you used a partial substitute (e.g., a
related but not perfectly matched tissue), say so explicitly in the methods
section — don't let the deliverable imply a cleaner match than what you
actually had.
