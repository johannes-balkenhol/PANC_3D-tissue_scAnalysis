# PANC_3D-tissue_scAnalysis

Single-cell RNA-seq analysis pipeline for a **3D PANC-1 pancreatic tumour tissue model**, from raw sequencing through trajectory-coupled dynamic network topology to cross-validation in a 726,107-cell patient atlas.

This repository contains the complete, ordered analysis code for:

> **3D tissue model to patient atlas: dynamic network topology reveals PDAC chemoresistance bottlenecks**
> Balkenhol J., Almasi M., et al. *npj Systems Biology and Applications* (under review, 2026).

---

## What this analysis does

PANC-1 cells were cultured on a decellularised porcine jejunal scaffold (SISmuc), treated under four conditions (control, gemcitabine, TGF-β1, gemcitabine + TGF-β1), and profiled by CellPlex-multiplexed 10x single-cell RNA-seq. The pipeline:

1. builds and QC-filters the single-cell object,
2. derives cell-state clusters and pseudotime trajectories,
3. tracks how **protein–protein interaction network betweenness centrality shifts continuously across pseudotime** rather than comparing static snapshots,
4. identifies an emergent **CDK1–CDKN1A–WEE1 bottleneck** arising only where G1→S progression and TGF-β1-induced EMT co-occur, and
5. cross-examines the resulting signatures in an independent PDAC patient atlas.

---

## Repository layout

```
notebooks/          ordered analysis pipeline (run top to bottom)
  00_*  environment setup, CellRanger multi, H5AD construction
  01_*  QC, filtering, normalisation
  02_*  dimension reduction & Leiden clustering
  03_*  pseudotime / trajectory inference
  04_*  differential expression, GSEA, gemcitabine-survivor analysis
  05_*  network construction (OmniPath), dynamic betweenness, bottleneck + KO
  06_*  patient-atlas validation
  07_*  publication figures (Fig. 5, Fig. S9, S10, S11)

scripts/            helper scripts (data deposition, repo curation)
envs/               conda environment specification
docs/               supplementary documentation
```

Notebooks are numbered in **execution order**. Each stage consumes the output of the previous one; intermediate objects are written to the paths documented at the top of each notebook.

---

## Data availability

| Resource | Location | Notes |
|---|---|---|
| **Raw sequencing data** (FASTQ) | ArrayExpress **E-MTAB-XXXXX** | Two libraries deposited as `mixed/pooled` samples: gene-expression (GEX) and CellPlex (CP). |
| **Processed AnnData** | ArrayExpress **E-MTAB-XXXXX** (processed file) | `PANC3D_PANC-1_3D-SISmuc_scRNAseq_processed.h5ad` — the object underlying every figure. |
| **Barcode → sample mapping** | ArrayExpress **E-MTAB-XXXXX** (processed file) | `PANC3D_barcode_to_sample_mapping.tsv` — required because the libraries are CellPlex-multiplexed; assigns each cell barcode to its biological sample. |
| **Patient atlas (external)** | Zenodo [10.5281/zenodo.14199536](https://doi.org/10.5281/zenodo.14199536) | Loveless & Steele, *Single Cell RNAseq Pancreatic Cancer Atlas*. |
| **Interactome** | [OmniPath](https://omnipathdb.org/) | Directed, signed PPI; curation effort ≥ 3. |
| **Reference genome** | `refdata-gex-GRCh38-2020-A` | 10x Genomics. |

> **Replace `E-MTAB-XXXXX` with the accession once ArrayExpress issues it.**

### Experimental design (CellPlex multiplexing)

Eight biological samples were pooled into a single 10x run:

| CMO | Sample | Condition | Culture |
|---|---|---|---|
| CMO301 | CTRL_1 | control | 3D |
| CMO302 | CTRL_2 | control | 3D |
| CMO304 | GEM_2 | gemcitabine | 3D |
| CMO305 | TGFb1_1 | TGF-β1 | 3D |
| CMO306 | TGFb1_2 | TGF-β1 | 3D |
| CMO307 | TGFb1_GEM_1 | gemcitabine + TGF-β1 | 3D |
| CMO308 | TGFb1_GEM_2 | gemcitabine + TGF-β1 | 3D |
| CMO309 | CTRL_2D | control | 2D (excluded from the 3D analysis) |

CMO303 was not used; there is a single gemcitabine replicate (GEM_2).

---

## Reproducing the analysis

```bash
git clone https://github.com/johannes-balkenhol/PANC_3D-tissue_scAnalysis.git
cd PANC_3D-tissue_scAnalysis

conda env create -f envs/environment.yml
conda activate panc3d

jupyter lab           # then run notebooks/ in numerical order
```

Download the processed AnnData from ArrayExpress and point the path variable at the top of `01_01` (or later, if starting mid-pipeline) at it.

### Key software

`scanpy` · `anndata` · `scFates` · `Palantir` · `PHATE` · `igraph` · `OmniPath` · `GSEApy` · `Scrublet` · `numpy` · `scipy` · `pandas` · `matplotlib` · `seaborn`

Exact pinned versions are in `envs/environment.yml`.

---

## FAIR statement

- **Findable** — code archived on GitHub with a persistent DOI via Zenodo (see *Citation*); data deposited in ArrayExpress with a stable accession; both cross-referenced in the manuscript.
- **Accessible** — code openly available under the MIT licence; raw and processed data openly available from ArrayExpress without restriction.
- **Interoperable** — data in community-standard formats (FASTQ, AnnData `.h5ad`, TSV); gene identifiers as Ensembl IDs and HGNC symbols; networks exported as GraphML.
- **Reusable** — provenance documented per notebook, pinned conda environment, explicit sample-level metadata, and a permissive licence for both code and data reuse.

---

## Licence

Code in this repository is released under the **MIT Licence** (see `LICENSE`).

Data deposited in ArrayExpress are released under the ArrayExpress terms of use. The external patient atlas and OmniPath retain their own respective licences.

---

## Citation

If you use this code, please cite the manuscript:

```bibtex
@article{balkenhol2026panc3d,
  title   = {3D tissue model to patient atlas: dynamic network topology
             reveals PDAC chemoresistance bottlenecks},
  author  = {Balkenhol, Johannes and Almasi, Maryam and Dandekar, Gudrun
             and Dandekar, Thomas},
  journal = {npj Systems Biology and Applications},
  year    = {2026},
  note    = {under review}
}
```

Please also cite the data deposit (**E-MTAB-XXXXX**) and, where relevant, the upstream resources (OmniPath; Loveless *et al.* atlas).

---

## Contact

**Johannes Balkenhol** — johannes.balkenhol@uni-wuerzburg.de
Department of Bioinformatics, Biozentrum, University of Würzburg, Am Hubland, 97074 Würzburg, Germany
