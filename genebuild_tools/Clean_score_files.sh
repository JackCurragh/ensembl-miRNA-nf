# Clean up the data- some outputs had weird lines at the end that I could not reproduce on my machine
# Remove the last line of the csv and the second entry of the json 

HEATMAPS='/nfs/production/flicek/ensembl/genebuild/jackt/projects/data/mirmachine/*/results/predictions/heatmap/'

# Ensure the outputs are exactly as we want them
for file in ${HEATMAPS}mirmachine_scores.csv; do 
        head -n 2 $file > $file.tmp
        mv $file.tmp $file
        # add to csv file
        tail -n 1 $file >> ./mirmachine_scores.csv
done

for file in ${HEATMAPS}mirmachine_scores.json; do 
        jq '.[0]' $file > $file.tmp
        mv $file.tmp $file
done
