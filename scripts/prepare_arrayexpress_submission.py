#!/usr/bin/env python3
"""
Prepare the ArrayExpress processed-data deposit for PANC-3D.

Produces two files, both derived ONLY from our own final AnnData object
(no dependency on any external/legacy CellRanger directory):

  1. PANC3D_PANC-1_3D-SISmuc_scRNAseq_processed.h5ad
       The final processed AnnData: normalised counts, QC-filtered,
       with cluster / pseudotime / condition annotation. This is the
       object underlying every figure in the manuscript.

  2. PANC3D_barcode_to_sample_mapping.tsv
       Per-cell-barcode assignment to the individual biological samples
       that were pooled in the CellPlex-multiplexed library, plus their
       metadata. Required by ArrayExpress curation because the two
       deposited libraries (GEX, CellPlex) are annotated mixed/pooled.

USAGE
-----
  python prepare_arrayexpress_submission.py \
      --h5ad   /storage/users/data/PANC/H5AD_file/adata_filtered_no2D_hvg_clust_time4_clust_t-bin.h5ad \
      --outdir ./arrayexpress_submission

  # inspect obs columns first if unsure:
  python prepare_arrayexpress_submission.py --h5ad <file> --inspect
"""

import argparse
import os
import sys

import pandas as pd
import scanpy as sc

# --------------------------------------------------------------------------
# Sample metadata, taken from our CellRanger multi config (cellRanger_PDAC_v3)
# NOTE: CMO303 was not used -- only one gemcitabine replicate (GEM_2) exists.
#       CTRL_2D is the 2D-culture control and is EXCLUDED from the 3D analysis.
# --------------------------------------------------------------------------
SAMPLE_META = {
    "CTRL_1":      dict(cmo="CMO301", condition="control",     treatment="none",
                        culture="3D", replicate="1"),
    "CTRL_2":      dict(cmo="CMO302", condition="control",     treatment="none",
                        culture="3D", replicate="2"),
    "GEM_2":       dict(cmo="CMO304", condition="GEM",         treatment="gemcitabine",
                        culture="3D", replicate="2"),
    "TGFb1_1":     dict(cmo="CMO305", condition="TGFb1",       treatment="TGF-beta1",
                        culture="3D", replicate="1"),
    "TGFb1_2":     dict(cmo="CMO306", condition="TGFb1",       treatment="TGF-beta1",
                        culture="3D", replicate="2"),
    "TGFb1_GEM_1": dict(cmo="CMO307", condition="TGFb1_GEM",   treatment="gemcitabine + TGF-beta1",
                        culture="3D", replicate="1"),
    "TGFb1_GEM_2": dict(cmo="CMO308", condition="TGFb1_GEM",   treatment="gemcitabine + TGF-beta1",
                        culture="3D", replicate="2"),
    "CTRL_2D":     dict(cmo="CMO309", condition="control_2D",  treatment="none",
                        culture="2D", replicate="1"),
}

COMMON = dict(
    organism="Homo sapiens",
    cell_line="PANC-1",
    cell_type="pancreatic ductal adenocarcinoma cell line",
    scaffold="decellularised porcine jejunal small intestinal submucosa (SISmuc)",
    multiplexing="10x Genomics CellPlex (CMO)",
    library_gex="SCC0019_Dandekar_GEX_H3",
    library_cellplex="SCC0019_Dandekar_CP_C2",
    reference_genome="refdata-gex-GRCh38-2020-A",
)

# candidate obs columns that may hold the per-cell sample label
SAMPLE_COL_CANDIDATES = [
    "sample", "sample_id", "Sample", "condition", "Condition",
    "orig.ident", "batch", "group", "Group",
]


def pick_sample_column(adata):
    for c in SAMPLE_COL_CANDIDATES:
        if c in adata.obs.columns:
            vals = set(map(str, adata.obs[c].unique()))
            # does it look like our sample IDs?
            if vals & set(SAMPLE_META):
                return c
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True, help="final processed AnnData (.h5ad)")
    ap.add_argument("--outdir", default="arrayexpress_submission")
    ap.add_argument("--sample-col", default=None,
                    help="obs column holding the biological sample ID "
                         "(auto-detected if omitted)")
    ap.add_argument("--inspect", action="store_true",
                    help="just print obs columns + value counts and exit")
    args = ap.parse_args()

    print(f"Reading {args.h5ad} ...")
    adata = sc.read_h5ad(args.h5ad)
    print(f"  {adata.n_obs:,} cells x {adata.n_vars:,} genes")

    if args.inspect:
        print("\nobs columns:")
        for c in adata.obs.columns:
            n = adata.obs[c].nunique()
            head = list(map(str, adata.obs[c].unique()[:8]))
            print(f"  {c:30s}  n_unique={n:<6d}  e.g. {head}")
        return

    col = args.sample_col or pick_sample_column(adata)
    if col is None:
        sys.exit("ERROR: could not auto-detect the sample column.\n"
                 "Run with --inspect to list obs columns, then pass --sample-col.")
    print(f"Using obs column '{col}' as the biological sample label.")

    os.makedirs(args.outdir, exist_ok=True)

    # ---- 1. barcode -> sample mapping table -------------------------------
    m = pd.DataFrame({
        "cell_barcode": adata.obs_names.astype(str),
        "sample_id": adata.obs[col].astype(str).values,
    })

    def annot(sid):
        meta = SAMPLE_META.get(sid)
        if meta is None:
            return pd.Series(dict(cmo_tag="NA", condition=sid, treatment="NA",
                                  culture="NA", replicate="NA"))
        return pd.Series(dict(cmo_tag=meta["cmo"], condition=meta["condition"],
                              treatment=meta["treatment"], culture=meta["culture"],
                              replicate=meta["replicate"]))

    m = pd.concat([m, m["sample_id"].apply(annot)], axis=1)
    for k, v in COMMON.items():
        m[k] = v

    cols = ["cell_barcode", "sample_id", "cmo_tag", "condition", "treatment",
            "culture", "replicate", "organism", "cell_line", "cell_type",
            "scaffold", "multiplexing", "reference_genome",
            "library_gex", "library_cellplex"]
    map_path = os.path.join(args.outdir, "PANC3D_barcode_to_sample_mapping.tsv")
    m[cols].to_csv(map_path, sep="\t", index=False)
    print(f"\nWrote {map_path}  ({len(m):,} barcodes)")
    print("\nCells per biological sample:")
    print(m["sample_id"].value_counts().to_string())

    # ---- 2. clean, well-named processed AnnData ---------------------------
    out_h5ad = os.path.join(
        args.outdir, "PANC3D_PANC-1_3D-SISmuc_scRNAseq_processed.h5ad")
    adata.uns["title"] = ("PANC-1 3D SISmuc tissue model, scRNA-seq: control, "
                          "gemcitabine, TGF-beta1, gemcitabine+TGF-beta1")
    adata.uns["arrayexpress_libraries"] = [COMMON["library_gex"],
                                           COMMON["library_cellplex"]]
    adata.uns["barcode_sample_mapping_file"] = os.path.basename(map_path)
    adata.write_h5ad(out_h5ad, compression="gzip")
    print(f"\nWrote {out_h5ad}")

    print("\nUpload BOTH files to Annotare as PROCESSED DATA FILES and attach "
          "them to the GEX library sample (SCC0019_Dandekar_GEX_H3).")


if __name__ == "__main__":
    main()
