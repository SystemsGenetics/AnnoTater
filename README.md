# AnnoTater

![AnnoTater Logo](https://raw.githubusercontent.com/SystemsGenetics/AnnoTater/refs/heads/master/docs/images/AnnoTater-Logo.png)


[![GitHub Actions CI Status](https://github.com/systemsgenetics/annotater/actions/workflows/ci.yml/badge.svg)](https://github.com/systemsgenetics/annotater/actions/workflows/ci.yml)
[![GitHub Actions Linting Status](https://github.com/systemsgenetics/annotater/actions/workflows/linting.yml/badge.svg)](https://github.com/systemsgenetics/annotater/actions/workflows/linting.yml)
[![nf-test](https://img.shields.io/badge/unit_tests-nf--test-337ab7.svg)](https://www.nf-test.com)
[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A524.04.2-23aa62.svg)](https://www.nextflow.io/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![run with singularity](https://img.shields.io/badge/run%20with-singularity-1d355c.svg?labelColor=000000)](https://sylabs.io/docs/)
<!-- [![Launch on Seqera Platform](https://img.shields.io/badge/Launch%20%F0%9F%9A%80-Seqera%20Platform-%234256e7)](https://cloud.seqera.io/launch?pipeline=https://github.com/systemsgenetics/annotater) -->
<!--[![Cite with Zenodo](http://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-1073c8?labelColor=000000)](https://doi.org/10.5281/zenodo.XXXXXXX) -->
<!-- [![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/) -->


## Introduction

AnnoTater AnnoTater is a whole or partial genome functional annotation workflow built using Nextflow. It takes a set of protein coding gene sequences (either in nucleotide or protein FASTA format) and runs InterProScan; BLAST vs UniProt SwissProt, NCBI NR, NCBI RefSeq, OrthoDB and StringDB in order to provide a first pass set of annotations for genes.

AnnoTater is constructed using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies.


<!-- Include a figure that guides the user through the major workflow steps. Many nf-core
     workflows use the "tube map" design for that. See https://nf-co.re/docs/contributing/design_guidelines#examples for examples.   -->

AnnoTater provides the following steps:

1. Homology searching against specified databases using Diamond BLAST ([`Diamond`](https://github.com/bbuchfink/diamond)). Supported databases include:
   - NCBI nr
   - NCBI RefSeq
   - ExPASy SwissProt
   - ExPASy Trembl
   - STRING database
2. Execution of [InterProScan](https://interproscan-docs.readthedocs.io/en/latest/)

## Usage

1. Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=25.04.07`)

1. Install any of [`Docker`](https://docs.docker.com/engine/installation/), [`Singularity`](https://www.sylabs.io/guides/3.0/user-guide/), [`Podman`](https://podman.io/), [`Shifter`](https://nersc.gitlab.io/development/shifter/how-to-use/) or [`Charliecloud`](https://hpc.github.io/charliecloud/) for full pipeline reproducibility ([`Conda`](https://conda.io/miniconda.html) is currently not supported); see [docs](https://nf-co.re/usage/configuration#basic-configuration-profiles)),

1. Download the pipeline to access the database download script:

   ```console
   nextflow pull systemsgenetics/annotater
   ```

1. Download databases. AnnoTater requires reference databases which can take quite a while to download and consume large amounts of storage. Use the included `download.py` script to retrieve and index the databases:

   ```console
   # List available datasets
   python3 ~/.nextflow/assets/systemsgenetics/annotater/bin/download.py --list --outdir /path/to/databases

   # Download specific datasets (comma-separated)
   python3 ~/.nextflow/assets/systemsgenetics/annotater/bin/download.py --outdir /path/to/databases --datasets interproscan,uniprot_sprot,nr

   # Download all datasets
   python3 ~/.nextflow/assets/systemsgenetics/annotater/bin/download.py --outdir /path/to/databases --datasets interproscan,panther,nr,refseq_plant,orthodb,string-db,uniprot_sprot,uniprot_trembl

   # Force re-download if datasets already exist
   python3 ~/.nextflow/assets/systemsgenetics/annotater/bin/download.py --outdir /path/to/databases --datasets interproscan --reset
   ```

   Available datasets include:
   - `interproscan` - InterProScan 5.75-106.0 with protein domain databases
   - `panther` - PANTHER database for InterProScan
   - `nr` - NCBI Non-Redundant protein database
   - `refseq_plant` - NCBI RefSeq plant protein sequences
   - `orthodb` - OrthoDB orthologous protein groups *(analysis under construction)*
   - `string-db` - STRING database protein interactions *(analysis under construction)*
   - `uniprot_sprot` - UniProt Swiss-Prot curated proteins
   - `uniprot_trembl` - UniProt TrEMBL unreviewed proteins

   > **Note**: Database downloads can be very large (10s-100s of GB) and may take hours to complete. The script supports resuming interrupted downloads.
   >
   > **Best Practice**: On multi-user systems, it is recommended to download databases to a shared location (e.g., `/shared/databases/annotater/` or `/opt/databases/annotater/`) that is accessible to all users. This prevents duplicate downloads and saves significant storage space, as multiple users can reference the same database files in their workflow runs.

1. Start running your own analysis!

   ```console
   nextflow run systemsgenetics/annotater \
       -profile <docker/singularity/podman/shifter/charliecloud/conda/institute> \
       --batch_size 100 \
       --input <fasta file> \
       --data_sprot <directory with swissprot diamond index> \
       --data_refseq <directory with refseq diamond index> \
       --data_ipr <directory with InterProScan data>

   ```

   **Available database arguments** (add any combination you've downloaded):
   - `--data_ipr <path>` - InterProScan database directory
   - `--data_sprot <path>` - UniProt Swiss-Prot database directory
   - `--data_trembl <path>` - UniProt TrEMBL database directory
   - `--data_nr <path>` - NCBI NR database directory
   - `--data_refseq <path>` - NCBI RefSeq database directory
   - `--data_orthodb <path>` - OrthoDB database directory *(experimental)*
   - `--data_string <path>` - STRING database directory *(experimental)*
   - `--enzyme_dat <path>` - Enzyme.dat file for EC number extraction (used with SwissProt)

   **Additional options:**
   - `--batch_size <number>` - Number of sequences to process per batch (default: 5)
   - `--seq_type <pep|nuc>` - Input sequence type: protein or nucleotide (default: pep)
   - `--taxonomy_ID <number>` - NCBI Taxonomy ID for the species (used by STRING database analysis)

## Output Format

AnnoTater produces several types of output files for functional annotation:

### Directory Structure
The pipeline outputs are organized in the specified output directory:
```
results/
├── blast/
│   ├── {prefix}_uniprot_sprot.blast.txt
│   ├── {prefix}_uniprot_trembl.blast.txt
│   ├── {prefix}_nr.blast.txt
│   └── {prefix}_refseq_plant.blast.txt
├── interproscan/
│   ├── {prefix}.IPR_mappings.txt
│   ├── {prefix}.GO_mappings.txt
│   └── {prefix}.tsv
├── ec_numbers/
│   └── {prefix}_EC_mappings.txt (if using SwissProt with enzyme.dat)
├── orthodb/
│   └── ortholog_results/ (experimental)
├── string/
│   └── interaction_results/ (experimental)
└── pipeline_info/
    ├── execution_report.html
    ├── execution_timeline.html
    └── annotater_software_versions.yml
```

### BLAST Results
For each database searched (SwissProt, TrEMBL, NR, RefSeq), the pipeline generates:
- **Combined BLAST results**: `{prefix}_{database}.blast.txt` - Tab-separated file containing all BLAST hits with detailed alignment information
- **Raw BLAST XML**: Individual XML files for each batch, later combined

### InterProScan Results
InterProScan analysis produces comprehensive functional annotation files:
- **IPR mappings**: `{prefix}.IPR_mappings.txt` - Tab-separated file mapping genes to InterPro entries
  ```
  Gene            IPR         Description
  LOC_Os01g01010  IPR001841   Zinc finger, RING-type
  LOC_Os01g01010  IPR013083   Zinc finger, RING/FYVE/PHD-type
  ```

- **GO mappings**: `{prefix}.GO_mappings.txt` - Tab-separated file mapping genes to Gene Ontology terms
  ```
  Gene            GO
  LOC_Os01g01010  GO:0005507
  LOC_Os01g01010  GO:0016491
  ```

- **Combined TSV**: `{prefix}.tsv` - Complete InterProScan output with all annotations including domains, signatures, and functional classifications

### Database-Specific Notes
- **OrthoDB analysis**: *Currently under construction*
- **STRING database analysis**: *Currently under construction*
- **EC number extraction**: Generated when using SwissProt database with enzyme.dat file


> [!WARNING]
> Please provide pipeline parameters via the CLI or Nextflow `-params-file` option. Custom config files including those provided by the `-c` Nextflow option can be used to provide any configuration _**except for parameters**_; see [docs](https://nf-co.re/docs/usage/getting_started/configuration#custom-configuration-files).

## Credits

AnnoTater and was written by the [Ficklin Computational Biology Team](http://ficklinlab.cahnrs.wsu.edu/) at [Washington State University](http://www.wsu.edu). Development of AnnoTater was initially funded by the U.S. National Science Foundation (NSF) Award [#1659300](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1659300&HistoricalAwards=false).


## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).

## Citations

AnnoTater is currently unpublished. For now, please use the GitHub URL when referencing. An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.

This pipeline uses code and infrastructure developed and maintained by the [nf-core](https://nf-co.re) community, reused here under the [MIT license](https://github.com/nf-core/tools/blob/main/LICENSE).

> **The nf-core framework for community-curated bioinformatics pipelines.**
>
> Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.
>
> _Nat Biotechnol._ 2020 Feb 13. doi: [10.1038/s41587-020-0439-x](https://dx.doi.org/10.1038/s41587-020-0439-x).
