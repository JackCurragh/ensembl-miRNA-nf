# ensembl-miRNA-nf
miRNA Detection workflow developed for genebuild team at Ensembl


## Project Structure
│\
├── README.md                                       \
├── LICENSE                                         \
├── main.nf                                         \
├── nextflow.config                                 \
├── params.config                                   \
│                                                   \
├── conf                                            \
│   ├── slurm.config                                    
│   └── standard.config                             \
│\
├── modules                                         \
│   └── local                                       \
│       ├── mirMachine_node_matcher.nf              \
│       └── rapid.nf                                \
│                                                   \
├── scripts                                         \        
│   ├── match_busco_lineage.py                      \
│   ├── match_clade.py                              \
│   └── rapid_fetch.py                              \
│                                                   \
└── subworkflows                                    \
    └── local                                       \
        └── mirMachine.nf                           

# To Do
- [ ] Solve conda environment issue
- [ ] Singularity issue for checking nodes
- [ ] Check that outputs are published correctly