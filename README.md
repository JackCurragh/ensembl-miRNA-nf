# ensembl-miRNA-nf
miRNA Detection workflow developed for genebuild team at Ensembl


## Project Structure
│<br />
├── README.md                                       #<br />
├── LICENSE                                         #<br />
├── main.nf                                         #<br />
├── nextflow.config                                 #<br />
├── params.config                                   #<br />
│                                                   <br />
├── conf                                            #<br />
│   ├── slurm.config                                #<br />    
│   └── standard.config                             #<br />
│<br />
├── modules                                         #<br />
│   └── local                                       #<br />
│       ├── mirMachine_node_matcher.nf              #<br />
│       └── rapid.nf                                #<br />
│                                                   <br />
├── scripts                                         #<br />        
│   ├── match_busco_lineage.py                      #<br />
│   ├── match_clade.py                              #<br />
│   └── rapid_fetch.py                              #<br />
│                                                   <br />
└── subworkflows                                    #<br />
    └── local                                       #<br />
        └── mirMachine.nf                           #<br />

# To Do
[] Solve conda environment issue
[] Singularity issue for checking nodes
[] Check that outputs are published correctly