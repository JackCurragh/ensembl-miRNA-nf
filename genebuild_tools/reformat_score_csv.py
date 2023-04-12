'''
Produce a csv file with the following columns:
    - Scientific Name
    - Accession
    - analysis_node
    - filtered_total_count
    - filtered_microRNA_score
    - filtered_no_hits
    - unfiltered_total_count
    - unfiltered_microRNA_score
    - filtered_out_families
'''

import argparse
import pandas as pd
import os 
import glob

def get_csv_paths(dir: str) -> list:
    '''
    Return a list of paths to csv files in the given directory

    Input: directory path

    Output: list of csv file paths
    '''
    path = f"{dir}/*/results/predictions/heatmap/mirmachine_score.csv"
    return list(glob.glob(path))

def parse_csv(path: str) -> dict:
    '''
    Read in the mirmachine scores csv and return a dataframe with the relevant columns
    '''
    df = pd.read_csv(path)
    name_accession_list = path.split('/')[-5].split('_')
    scientific_name = ' '.join(name_accession_list[:-2])
    accession = '_'.join(name_accession_list[-2:])
    analysis_node = df['analysis_node'][0]
    filtered_total_count = df['filtered_total_count'][0]
    filtered_microRNA_score = df['filtered_microRNA_score'][0]
    filtered_no_hits = df['filtered_no_hits'][0]
    unfiltered_total_count = df['unfiltered_total_count'][0]
    unfiltered_microRNA_score = df['unfiltered_microRNA_score'][0]
    filtered_out_families = df['filtered_out_families'][0]

    return {
        'Scientific Name': scientific_name, 
        'Accession': accession, 
        'analysis_node': analysis_node, 
        'filtered_total_count': filtered_total_count, 
        'filtered_microRNA_score': filtered_microRNA_score, 
        'filtered_no_hits': filtered_no_hits, 
        'unfiltered_total_count': unfiltered_total_count, 
        'unfiltered_microRNA_score': unfiltered_microRNA_score, 
        'filtered_out_families': filtered_out_families}



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='MirMachine parent directory')
    parser.add_argument('-o', '--output', help='Output csv file')
    args = parser.parse_args()

    output_df = pd.DataFrame(columns=['Scientific Name', 'Accession', 'analysis_node', 'filtered_total_count', 'filtered_microRNA_score', 'filtered_no_hits', 'unfiltered_total_count', 'unfiltered_microRNA_score', 'filtered_out_families'])
    csv_paths = get_csv_paths(args.dir)

    for file in csv_paths:
        new_row = parse_csv(file)
        output_df = output_df.append(new_row, ignore_index=True)

    # Write the new csv file
    output_df.to_csv(args.output, index=False)

if __name__ == '__main__':
    main()