"""Lightweight GEO series matrix parser (no GEOparse dependency needed).

Series matrix format:
  - Header lines starting with "!Series_" describe the study itself
    (title, summary, platform) - read these FIRST to verify the dataset
    actually matches your research question before parsing anything else.
  - Header lines starting with "!Sample_..." give per-sample metadata
    (tab-separated, values quoted). "!Sample_geo_accession" gives GSM ids
    in column order. "!Sample_characteristics_ch1" usually carries the
    disease/tissue/group labels you need for group comparisons.
  - "!series_matrix_table_begin" / "!series_matrix_table_end" bound the
    expression matrix: first row is header (ID_REF + GSM ids), subsequent
    rows are probe_id + values.

Usage:
    from parse_geo_series_matrix import parse_series_matrix, print_series_summary
    print_series_summary("data/GSEXXXXX_series_matrix.txt")   # verify first
    expr, meta = parse_series_matrix("data/GSEXXXXX_series_matrix.txt")
"""
import pandas as pd
import numpy as np


def print_series_summary(path):
    """Print the study title/summary/design so you can verify the dataset
    actually matches your research question BEFORE running any analysis.
    Do not skip this - see references/dataset_verification.md."""
    with open(path, encoding="latin-1") as f:
        for line in f:
            if line.startswith("!Series_title") or line.startswith("!Series_summary") \
               or line.startswith("!Series_overall_design") or line.startswith("!Series_platform_id"):
                print(line.strip())
            if line.startswith("!series_matrix_table_begin"):
                break


def parse_series_matrix(path):
    sample_meta = {}
    table_start = None
    table_end = None
    with open(path, encoding="latin-1") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("!Sample_"):
            parts = line.rstrip("\n").split("\t")
            key = parts[0][len("!Sample_"):]
            values = [v.strip('"') for v in parts[1:]]
            if key in sample_meta:
                n = 2
                while f"{key}_{n}" in sample_meta:
                    n += 1
                key = f"{key}_{n}"
            sample_meta[key] = values
        if line.startswith("!series_matrix_table_begin"):
            table_start = i + 1
        if line.startswith("!series_matrix_table_end"):
            table_end = i
            break

    if table_start is None or table_end is None:
        raise ValueError(f"Could not find data table markers in {path}")

    table_lines = lines[table_start:table_end]
    header = table_lines[0].rstrip("\n").split("\t")
    header = [h.strip('"') for h in header]

    rows = []
    ids = []
    for line in table_lines[1:]:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        ids.append(parts[0].strip('"'))
        rows.append([np.nan if v in ("", "null", "NA") else float(v) for v in parts[1:]])

    expr = pd.DataFrame(rows, index=ids, columns=header[1:])
    expr.index.name = "ID_REF"

    meta = pd.DataFrame(sample_meta)
    meta.index = meta["geo_accession"]
    meta.index.name = "GSM"

    return expr, meta


if __name__ == "__main__":
    import sys
    print_series_summary(sys.argv[1])
    expr, meta = parse_series_matrix(sys.argv[1])
    print("Expression matrix:", expr.shape)
    print("Raw value range:", np.nanmin(expr.to_numpy()), "-", np.nanmax(expr.to_numpy()))
    print("Sample metadata columns:", list(meta.columns))
    if "characteristics_ch1" in meta.columns:
        print(meta["characteristics_ch1"].value_counts())
