# Clean up the data- some outputs had weird lines at the end that I could not reproduce on my machine
# Remove the last line of the csv and the second entry of the json 

# cd to the parent directory where each species is in a separate subdirectory
# eg. /nfs/production/flicek/ensembl/genebuild/jackt/projects/data/mirmachine/

PARENT_DIR=$PWD
for file in ${PARENT_DIR}/*/results/predictions/heatmap/mirmachine_scores.csv; do
    head -n 2 $file > $file.tmp
    mv $file.tmp $file
done

for file in */results/predictions/heatmap/mirmachine_scores.json; do
    jq '.[0]' $file > $file.tmp
    mv $file.tmp $file
done