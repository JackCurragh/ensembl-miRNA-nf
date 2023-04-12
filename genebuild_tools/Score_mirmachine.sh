# Description: Score mirmachine predictions

SCORE='/hps/software/users/ensembl/repositories/jackt/ensembl-mirna-nf/scripts/mircroRNA_scoring.py'
HEATMAPS='/nfs/production/flicek/ensembl/genebuild/jackt/projects/data/mirmachine/*/results/predictions/heatmap/'

for file in "${HEATMAPS}*.csv"; do
        DIR="$(dirname "${file}")"
        OUTPUT="${DIR}/mirmachine_score.csv"
        bsub -Is -M 4096 python ${SCORE} -i ${file}  -o $OUTPUT --json &
done

