#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Curate scripts_beta -> a clean, ordered, non-redundant notebook pipeline.
#
# Run from the PANC_cancer project root, e.g.
#   cd /storage/users/job37yv/Projects/PANC_cancer
#   bash <this-script> /path/to/PANC_3D-tissue_scAnalysis
#
# Only notebooks that produce results in the published manuscript are kept.
# Backups (-bu), duplicates (Copy1), superseded variants, and exploratory
# dead-ends (scBonita, scPrint, STRING, KEGG) are deliberately excluded.
#
# IMPORTANT: notebook filenames are renamed to the FINAL published figure
# numbering:  S9 = betweenness overview, S10 = molecular gate, S11 = atlas.
# (The scripts_beta filenames still use the old, pre-revision numbering.)
# ---------------------------------------------------------------------------
set -euo pipefail

SRC="code/scripts_beta"
DEST="${1:?usage: build_repo_from_scripts_beta.sh <path-to-repo>}"
NB="$DEST/notebooks"
mkdir -p "$NB"

copy () {  # copy <source-basename> <target-basename>
  if [[ -f "$SRC/$1" ]]; then
    cp -v "$SRC/$1" "$NB/$2"
  else
    echo "  !! MISSING: $SRC/$1" >&2
  fi
}

echo "== 00  environment & ingestion =="
copy "001_Preprocessing of Environment.ipynb"                 "00_01_environment_setup.ipynb"
copy "002.0_Cellranger_processing.ipynb"                      "00_02_cellranger_multi.ipynb"
copy "002.1_Load_Data_and_create_H5ad_file_cleaned.ipynb"     "00_03_build_h5ad.ipynb"

echo "== 01  QC & normalisation =="
copy "003.0_QC_filtering_normalization.ipynb"                 "01_01_qc_filtering_normalisation.ipynb"

echo "== 02  dimension reduction & clustering =="
# 004.2 (no2D + HVG) is the version used for all published results
copy "004.2_DimensionReduction&Clustering_no2D_hvg.ipynb"     "02_01_dimred_clustering.ipynb"

echo "== 03  trajectory / pseudotime =="
copy "005.0_Pseudotime-v2.ipynb"                              "03_01_pseudotime_trajectories.ipynb"

echo "== 04  differential expression & enrichment =="
copy "008.0_DEG.ipynb"                                        "04_01_differential_expression.ipynb"
copy "007.0_Create_dictionary.ipynb"                          "04_02_gene_id_dictionary.ipynb"
copy "007.1_GSEA-time-leiden.ipynb"                           "04_03_gsea_pseudotime_leiden.ipynb"
copy "006.0_GEM_anaylsis.ipynb"                               "04_04_gemcitabine_survivor_analysis.ipynb"

echo "== 05  network construction & dynamic topology =="
copy "011.1_generate-network_nodes.ipynb"                     "05_01_network_nodes.ipynb"
copy "011.2_generate-network_edges_omnipath.ipynb"            "05_02_network_edges_omnipath.ipynb"
copy "011.7_generate-network_simple-analysis.ipynb"           "05_03_network_topology_betweenness.ipynb"
copy "011.4_network-modules_find-bottlennecks.ipynb"          "05_04_bottleneck_identification_ko.ipynb"
copy "011.3_gsea_on_network_modules.ipynb"                    "05_05_gsea_network_modules.ipynb"

echo "== 06  patient-atlas validation =="
copy "012_atlas-validation_ANALYSIS_CDK1-CDKN1A.ipynb"        "06_01_atlas_validation_analysis.ipynb"

echo "== 07  publication figures =="
copy "013_Fig5_axis-validation_PUBFIG.ipynb"                  "07_01_Fig5_axis_validation.ipynb"
copy "011.8_FigS10_betweenness_PUBFIG.ipynb"                  "07_02_FigS9_betweenness_overview.ipynb"
copy "011.9_FigS11_molecular-gate_PUBFIG.ipynb"               "07_03_FigS10_molecular_gate.ipynb"
copy "014_FigS9_atlas-multilevel_PUBFIG.ipynb"                "07_04_FigS11_atlas_multilevel.ipynb"

echo
echo "== EXCLUDED (redundant / superseded / not used in the manuscript) =="
cat <<'EOF'
  *-bu.ipynb                                   backups
  011.2_..._omnipath-Copy1.ipynb               byte-identical duplicate
  004.0_..._with2D / 004.1_..._no2D / 004.2_..._hvg   superseded by 004.2_no2D_hvg
  005.0_Pseudotime-v1*.ipynb                   superseded by v2
  007.1_GSEA.ipynb / -time / -time-milestones  superseded by -time-leiden
  009.*_PFA_*.ipynb, 010.1_results_summary     exploratory, not in manuscript
  011.3_..._scPrint / 011.4_scBonita /
  011.5_..._string / 011.6_..._kegg            alternative network sources, not used
  zz_OLD_Fig5-atlas-mix_SUPERSEDED_*           explicitly superseded
EOF

echo
echo "Done. Notebooks written to $NB"
echo "NOTE: figure notebooks were renamed to the FINAL published numbering"
echo "      (S9 = betweenness, S10 = gate schematic, S11 = atlas)."
echo "      The figure-internal captions/labels must match this too."
