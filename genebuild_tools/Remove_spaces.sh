# This command removes from the file and directory names any spaces, and replaces them with underscores.
#
# Usage: Remove_spaces.sh <path_to_data>
# Path to data should be the parent directory of the species directories

PATH_TO_DATA=$1

for file in ${PATH_TO_DATA}/*; do
    mv "$file" "${file// /_}"
done
