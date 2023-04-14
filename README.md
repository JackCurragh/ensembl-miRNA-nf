# ensembl-miRNA-nf
Automated MirMachine Based miRNA Detection workflow developed for genebuild team at Ensembl

## Deployment

### General

Default inputs to this Nextflow pipeline are specified in the params.config file. However, each can be overwritten when calling Nextflow:
Eg.
```
nextflow run main.nf --outdir /path/to/output_directory
```

This pipeline is designed to run MirMachine on a single organism at a time with automated FASTA retrieval and node assignment. It can be run using `lsf` or `slurm` by specifying them as the executor with `-profile <executor>`:

Eg. 
```
nextflow run main.nf -profile lsf 
```

All required software is installed in a singularity container that is specified within 'params.config'. This could be moved to being specified in nextflow.config but I had issues with this so it was easier to be able to specify different containers when calling Nextflow. 

### Genebuild
The `genebuild_tools` directory contains a set of scripts that will help run MirMachine on many organisms at a time using EBI resources. 

1. `Run_mirmachine.sh` - Ensures the Rapid list of assemblies/annotations is tab delimited and then runs the Nextflow pipeline on `lsf`. 
2. `Remove_spaces.sh` - The resulting directory names may contain spaces. This script addresses that making it easier to work with the resulting files.
3. `Score_mirmachine.sh` - Deploys the scoring script on all MirMachine results in a given directory. 
4. `Clean_score_files.sh` - Tidies up any atypical outputs and combines the scores into a file in the CWD 
5. `reformat_score_csv.py` - Produces a better results file that takes information from the files paths eg. `Ensembl_Rapid_Release-20_2_2023.csv`
6. `Add_to_ftp.sh` - Moves output files to ftp only moving files that have changed since last run.

Please note: these scripts (except the .py) were rewritten after I used them so there is potential for mistakes as they have not been tested on the full annotation set. 

### Note on containers: 
This is the least reproducibly part of how I managed this. I couldn't get MirMachine and Ete3 to build in the same container so the container definition files here are not sufficient. I have left them as a work in progress. 


The hack that I used was to pull the MirMachine container and install ete3 with pip inside that container. Sorry...
```
singularity pull https://depot.galaxyproject.org/singularity/mirmachine%3A0.2.12--pyhdfd78af_0

singularity run depot.galaxyproject.org-singularity-mirmachine%3A0.2.12--pyhdfd78af_0.img
Singularity> python -m pip install ete3 biopython numpy pandas six
```
