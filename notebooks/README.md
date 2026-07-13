# Analysis pipeline

Run the notebooks in numerical order. Each stage consumes the output of the
previous one.

| Stage | Notebook | Purpose |
|---|---|---|
| 00 | `00_01_environment_setup` | environment / dependency check |
| 00 | `00_02_cellranger_multi` | CellRanger `multi` (CellPlex demultiplexing) |
| 00 | `00_03_build_h5ad` | assemble the AnnData object |
| 01 | `01_01_qc_filtering_normalisation` | QC, doublet removal, normalisation |
| 02 | `02_01_dimred_clustering` | HVG, PCA, UMAP/FA2, Leiden clustering |
| 03 | `03_01_pseudotime_trajectories` | trajectory inference & pseudotime bins |
| 04 | `04_01_differential_expression` | DE between clusters / conditions |
| 04 | `04_02_gene_id_dictionary` | Ensembl ⇄ HGNC / UniProt mapping |
| 04 | `04_03_gsea_pseudotime_leiden` | GSEA across pseudotime and clusters |
| 04 | `04_04_gemcitabine_survivor_analysis` | GEM-survivor characterisation |
| 05 | `05_01_network_nodes` | expression-filtered network nodes |
| 05 | `05_02_network_edges_omnipath` | directed signed PPI edges (OmniPath) |
| 05 | `05_03_network_topology_betweenness` | betweenness per pseudotime bin |
| 05 | `05_04_bottleneck_identification_ko` | shortest-path overlap + knockout sims |
| 05 | `05_05_gsea_network_modules` | enrichment of network modules |
| 06 | `06_01_atlas_validation_analysis` | CDK1–CDKN1A axis in the patient atlas |
| 07 | `07_01_Fig5_axis_validation` | **Figure 5** |
| 07 | `07_02_FigS9_betweenness_overview` | **Figure S9** |
| 07 | `07_03_FigS10_molecular_gate` | **Figure S10** |
| 07 | `07_04_FigS11_atlas_multilevel` | **Figure S11** |

Figure numbering follows the published manuscript:
**S9** = betweenness overview, **S10** = molecular-gate schematic, **S11** = multi-level atlas.
