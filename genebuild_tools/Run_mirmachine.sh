# The Mirmachine pipeline is designed to run on a single species at a time.
# This is how to run the pipeline on codon for all species in the csv downloaded from rapid

# First set up the config file to ensure outputs are to the correct location
# Then run the pipeline
#
# Usage: Run_mirmachine.sh <path_to_csv>

MAIN_NF=/hps/software/users/ensembl/repositories/jackt/ensembl-mirna-nf/main.nf

# Check if the file is tab delimited
if head -n 1 $1 | grep -qP '\t'; then
    INPUT_FILE=$1
else
    echo "Convert to tab delimited"
    tr ',' '\t' < $1 > $1.tab
    INPUT_FILE=$1.tab
fi
fi

while IFS=$'\t' read -r -a entryArray; do 
        bsub -Is -M 4096 nextflow run ${MAIN_NF} -profile lsf --species "${entryArray[0]}" --accession "${entryArray[5]}" &
done < $INPUT_FILE
