MIRMACHINE_FTP_PATH="/nfs/production/flicek/ensembl/production/ensemblftp/rapid-release/species"
PATH_TO_DATA=$($1)

sudo -u genebuild mkdir -p ${MIRMACHINE_FTP_PATH}/
sudo -u genebuild rsync -ahvW ${PATH_TO_DATA}/*  ${MIRMACHINE_FTP_PATH}/ 
sudo -u genebuild find $MIRMACHINE_FTP_PATH -user genebuild -exec chmod g+w {} \;