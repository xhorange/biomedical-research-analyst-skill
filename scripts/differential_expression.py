"""Two-group differential expression for already-log-scaled, continuous
expression data (microarray intensities). NOT appropriate for raw RNA-seq
counts - see references/statistical_methods.md for why, and what to use
instead for count data.

Usage:
    from differential_expression import welch_de
    res = welch_de(expr, disease_samples, control_samples)
    res.to_csv("results/DEG_disease_vs_control.csv")
"""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


def welch_de(expr, group_a_samples, group_b_samples):
    """group_a = disease/treatment, group_b = control/reference.

    `expr` must already be log2-scale (check the series matrix's
    !Series_data_processing field and the raw value range before calling
    this - linear-scale intensities need log2(clip(x, lower=1)) first;
    already-log-scale processed signal should NOT be transformed again).

    Returns a DataFrame indexed like `expr` with log2FC (a vs b), raw
    p-value, BH-FDR, and per-group means - one row per probe/feature.
    Collapse to gene level afterwards (see `collapse_to_gene_level`).
    """
    a = expr[group_a_samples].to_numpy(dtype=float)
    b = expr[group_b_samples].to_numpy(dtype=float)
    mean_a = np.nanmean(a, axis=1)
    mean_b = np.nanmean(b, axis=1)
    log2fc = mean_a - mean_b
    t, p = stats.ttest_ind(a, b, axis=1, equal_var=False, nan_policy="omit")
    p = np.where(np.isnan(p), 1.0, p)
    _, fdr, _, _ = multipletests(p, method="fdr_bh")
    return pd.DataFrame({
        "log2FC": log2fc,
        "pvalue": p,
        "FDR": fdr,
        "mean_group_a": mean_a,
        "mean_group_b": mean_b,
    }, index=expr.index)


def collapse_to_gene_level(de_result, gene_symbol_series):
    """Join probe-level DE results to a gene-symbol annotation Series
    (index = probe/feature id, values = gene symbol) and collapse
    multi-mapping probes to one row per gene, keeping the probe with the
    largest absolute log2FC. Document this tie-breaking rule if you change
    it - it's a real methodological choice, not a neutral default."""
    res = de_result.join(gene_symbol_series.rename("GeneSymbol"), how="left")
    res = res.dropna(subset=["GeneSymbol"])
    res["absFC"] = res["log2FC"].abs()
    res = res.sort_values("absFC", ascending=False)
    gene_level = res.groupby("GeneSymbol").first().drop(columns=["absFC"])
    return gene_level.reset_index()


def summarize_sig(gene_level_df, fdr_cut=0.05, fc_cut=1.0, label=""):
    n_sig = ((gene_level_df["FDR"] < fdr_cut) & (gene_level_df["log2FC"].abs() >= fc_cut)).sum()
    print(f"{label}: {gene_level_df.shape[0]} genes tested, {n_sig} DEGs "
          f"(|log2FC|>={fc_cut}, FDR<{fdr_cut})")
    return n_sig
