#! /bin/bash

# This script is used to add the miRNA data to the FTP site
# 
# Usage: Add_to_ftp.sh <path_to_data>

MIRMACHINE_FTP_PATH="/nfs/production/flicek/ensembl/production/ensemblftp/rapid-release/species"
PATH_TO_DATA=$($1)

sudo -u genebuild mkdir -p ${MIRMACHINE_FTP_PATH}/
sudo -u genebuild rsync -ahvW ${PATH_TO_DATA}/*  ${MIRMACHINE_FTP_PATH}/ 
sudo -u genebuild find $MIRMACHINE_FTP_PATH -user genebuild -exec chmod g+w {} \;