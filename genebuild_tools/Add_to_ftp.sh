#! /bin/bash

# This script is used to add the miRNA data to the FTP site
# this should be run in a datamover interactive shell as genebuild
# 
# Usage: Add_to_ftp.sh <path_to_data>
# Path to data should be the parent directory of the species directories
# eg. /nfs/production/flicek/ensembl/genebuild/jackt/projects/data/mirmachine/

MIRMACHINE_FTP_PATH="/nfs/ftp/public/databases/ensembl/mirmachine/"
PATH_TO_DATA=$($1)

sudo -u genebuild rsync -ahvW --update --chown=genebuild:ensembl  ${PATH_TO_DATA}/*  ${MIRMACHINE_FTP_PATH}/ 