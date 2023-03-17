: '
This script is used to setup the container environment.

It can be called directly to setup the environment. It is a hacky way to bypass 
issues with the containers not executing right via Nextflow

'
#!/bin/bash

#Load Singularity

echo ""
echo "+-----------------------------------------+"
echo "| Loading singularity module               |"
echo "+-----------------------------------------+"
echo ""
module load singularity-3.7.0-gcc-9.3.0-dp5ffrp

# Setup singularity image
echo ""
echo "+-----------------------------------------+"
echo "| Setup Singularity Image                 |"
echo "+-----------------------------------------+"
echo ""
MIRMACHINE_URL="https://depot.galaxyproject.org/singularity/mirmachine%3A0.2.12--pyhdfd78af_0"
MIRMACHINE_IMAGE_NAME=$(echo $MIRMACHINE_URL | cut -d "/" -f 5 | cut -d ":" -f 1)

SINGULARITY_PATH=$(grep "cacheDir" nextflow.config | cut -d "=" -f 2 | tr -d " ")
SINGULARITY_PATH=$(echo $SINGULARITY_PATH | tr -d "'")

# Check if the singularity cache directory exists
if [[ -d $SINGULARITY_PATH ]]; then
    echo "Singularity cache directory already exists"
else
    mkdir $SINGULARITY_PATH
fi

# Check if the image already exists if not download it
if [[ -f ${SINGULARITY_PATH}/${MIRMACHINE_IMAGE_NAME} ]]; then
    echo "Singularity image already exists"
else
    echo "Downloading singularity image"
    singularity pull $MIRMACHINE_URL
    mv ${MIRMACHINE_IMAGE_NAME} ${SINGULARITY_PATH}/
fi

PWD=$(pwd)
MIRMACHINE_PATH=$PWD/$SINGULARITY_PATH/$MIRMACHINE_IMAGE_NAME


# Setup python virtual environment
echo ""
echo "+-----------------------------------------+"
echo "| Setup Python Virtual Environment        |"
echo "+-----------------------------------------+"
echo ""
if [[ -d venv ]]; then
    echo "Python virtual environment already exists"
else
    echo "Creating python virtual environment"
    python -m venv venv
fi
source venv/bin/activate
python -m pip install ete3 six numpy
deactivate
ETE_PATH="$PWD/venv/bin/python"

# Update Params.conf
echo ""
echo "+-----------------------------------------+"
echo "| Update Params.config                    |"
echo "+-----------------------------------------+"
echo ""
CONFIG_LINE="\tmirmachine_singularity = '$MIRMACHINE_PATH'\n\tete_python = '$ETE_PATH'\n}"
awk -v var="$CONFIG_LINE" '{gsub("}",var,$0); print}' params.config > output.txt
mv output.txt params.config
echo ""
echo "+-----------------------------------------+"
echo "| Setup Complete                          |"
echo "+-----------------------------------------+"
echo ""
