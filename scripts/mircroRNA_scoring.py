'''
Python script to score microRNA sequences. Based on ./microRNA_scoring.rmd By: Vanessa Paynter

Input file:
    - mirMachine Heatmap file
    - mirMachine metadata file

Output file:
    - species score file

    
Usage:
    python microRNA_scoring.py -i <input file> -m <metadata file> -o <output file> 

'''

import argparse
import pandas as pd
import numpy as np
import sys


def parse_heatmap(headmapt_csv_path: str) -> pd.DataFrame:
    '''
    Read in the mirMachine heatmap file and return a pandas dataframe. Convert the species column to uppercase.

    Input:
        headmapt_csv_path: str
            Path to the mirMachine heatmap file

    Output:
        heatmap: pd.DataFrame
            Pandas dataframe of the mirMachine heatmap file
    '''
    heatmap = pd.read_csv(headmapt_csv_path, sep=",", comment='#', header=None)
    heatmap.columns = ['species', 'mode' , 'family', 'node', 'tgff', 'filtered']
    # heatmap['species'] = heatmap['species'].str.upper()
    return heatmap

def parse_metadata(metadata_csv_path: str) -> pd.DataFrame:
    '''
    Read in the mirMachine metadata file and return a pandas dataframe

    Input:  
        metadata_csv_path: str  
            Path to the mirMachine metadata file    

    Output:
        metadata: pd.DataFrame
            Pandas dataframe of the mirMachine metadata file
    '''
    metadata = pd.read_csv(metadata_csv_path, sep=",", header=None)
    return metadata

def get_mirmachine_total_families_searched(heatmap_path: str) -> int:
    '''
    Get the total number of microRNA families searched for in mirMachine

    Input:
        heatmap_path: str
            Path to the mirMachine heatmap file

    Output:
        mirmachine_total_families_searched: int
            Total number of microRNA families searched for in mirMachine
    '''
    with open(heatmap_path) as f:
        for line in f.readlines():
            if line.startswith('# Total families searched'):
                mirmachine_total_families_searched = int(line.split(': ')[1].strip())
                break
    return mirmachine_total_families_searched


def create_filtered_score_df(heatmap: pd.DataFrame, mirmachine_total_families_searched) -> pd.DataFrame:
    '''
    Create a pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine

    Input:
        heatmap: pd.DataFrame
            Pandas dataframe of the mirMachine heatmap file

    Output:
        filtered_score_df: pd.DataFrame
            Pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine
    '''
    # Drop the 'tgff' column from the heatmap dataframe and remove any rows where the 'filtered' column is missing.
    filtered = heatmap.drop(columns=['tgff']).dropna(subset=['filtered'])

    # Group the dataframe by the 'species' column and count the number of non-missing values in the 'filtered' column for each group.
    filtered = filtered.groupby('species')['filtered'].count()

    # Divide the series by the total number of microRNA families searched for in mirMachine and multiply the result by 100.
    filtered_score = (filtered / mirmachine_total_families_searched) * 100

    # Convert the  series to a dataframe
    filtered_df = filtered.to_frame()

    # Add a new column to the 'unfiltered_df' dataframe with the 'filtered_score' series as its values.
    filtered_score_df = filtered_df.assign(filtered_microRNA_score=filtered_score)

    # Rename the 'filtered' column to 'filtered_total_count'
    filtered_score_df = filtered_score_df.rename(columns={'filtered': 'filtered_total_count'})

    return filtered_score_df

def calculate_unfiltered_score(heatmap: pd.DataFrame, mirmachine_total_families_searched) -> pd.DataFrame:
    '''
    Create a pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine

    Input:
        heatmap: pd.DataFrame
            Pandas dataframe of the mirMachine heatmap file

    Output:
        filtered_score_df: pd.DataFrame
            Pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine
    '''
    # Drop the 'filtered' column from the heatmap dataframe and remove any rows where the 'tgff' column is missing.
    unfiltered = heatmap.drop(columns=['filtered']).dropna(subset=['tgff'])

    # Group the 'unfiltered' dataframe by the 'species' column and count the number of non-missing values in the 'tgff' column for each group.
    unfiltered = unfiltered.groupby('species')['tgff'].count()

    # Divide the 'unfiltered' series by the total number of microRNA families searched for in mirMachine and multiply the result by 100.
    unfiltered_score = (unfiltered / mirmachine_total_families_searched) * 100

    # Convert the 'unfiltered' series to a dataframe and rename the column to 'unfiltered_total_count'.
    unfiltered_df = unfiltered.to_frame()

    # Add a new column to the 'unfiltered_df' dataframe with the 'unfiltered_score' series as its values.
    unfiltered_df = unfiltered_df.assign(unfiltered_microRNA_score=unfiltered_score)

    # Rename the 'filtered' column to 'filtered_total_count'
    unfiltered_df = unfiltered_df.rename(columns={'tgff': 'unfiltered_total_count'})

    return unfiltered_df


def get_filtered_out_families(mammals_heatmap: pd.DataFrame):
    '''
    Get the microRNA families that were filtered out of the mirMachine analysis

    Input:
        mammals_heatmap: pd.DataFrame

    Output:
        filtered_out_families: pd.DataFrame

    '''
    # Filter the DataFrame to only include rows where the 'filtered' column is NaN
    filtered_rows = mammals_heatmap.loc[pd.isna(mammals_heatmap['filtered']), ['species', 'family', 'tgff']]
    
    # Drop any rows with NaN values in the 'tgff' column
    filtered_rows = filtered_rows.dropna(subset=['tgff'])
    
    # Group the remaining rows by 'species', and concatenate the 'family' values into a comma-separated string
    filtered_out_families = filtered_rows.groupby('species')['family'].apply(lambda x: ', '.join(x))
    
    # Convert the resulting Series into a DataFrame with a column name of 'filtered_out_families'
    filtered_out_families = filtered_out_families.reset_index(name='filtered_out_families')
    
    return filtered_out_families

def get_filtered_no_hits(mammals_heatmap: pd.DataFrame):
    '''
    Get the microRNA families that had no hits in the mirMachine analysis

    Input:
        mammals_heatmap: pd.DataFrame

    Output:
        filtered_no_hits: pd.DataFrame
    '''
    # Select rows where 'filtered' column is missing and 'tgff' column is missing.
    missing_data = pd.isna(mammals_heatmap['filtered']) & mammals_heatmap[['tgff', 'filtered']].isna().all(axis=1)

    # Select the columns 'species', 'family', and 'filtered' from the filtered dataframe.
    selected_cols = ['species', 'family', 'filtered']
    filtered_missing = mammals_heatmap.loc[missing_data, selected_cols]

    # Group the resulting dataframe by 'species' and combine the 'family' values for each group into a comma-separated string.
    mammals_filtered_missing = filtered_missing.groupby('species')['family'].apply(lambda x: ', '.join(x)).reset_index(name='filtered_no_hits')
    return mammals_filtered_missing


def merge_and_output(filtered_score_df: pd.DataFrame, 
                     unfiltered_score_df: pd.DataFrame, 
                     analysis_node: str, 
                     family_ID: pd.DataFrame, 
                     mammals_filtered_missing: pd.DataFrame,
                     output_path: str,
                     json: str
                     ):
    '''
    Merge the filtered and unfiltered dataframes and output the final table

    Input:
        filtered_score_df: pd.DataFrame
            Pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine

        unfiltered_score_df: pd.DataFrame
            Pandas dataframe with the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine

        heatmap: pd.DataFrame
            Pandas dataframe of the mirMachine heatmap file

        mirmachine_total_families_searched: int
            Total number of microRNA families searched for in mirMachine

        output_path: str
            Path to the output file
    '''
    # Merge the filtered and unfiltered score dataframes using an outer join on 'species'
    mammals_score_df = pd.merge(filtered_score_df, unfiltered_score_df, how='outer', on='species')
    
    # Add a new column to the merged dataframe with the analysis node identifier
    mammals_score_df['analysis_node'] = analysis_node
    
    # Merge the resulting dataframe with the 'family_ID' dataframe using a left join on 'species'
    microRNA_score_table = pd.merge(mammals_score_df, family_ID, how='left', on='species')
    
    # Merge the resulting dataframe with the 'mammals_filtered_missing' dataframe using a left join on 'species'
    microRNA_score_table = pd.merge(microRNA_score_table, mammals_filtered_missing, how='left', on='species')
    
    # Round the 'filtered_microRNA_score' and 'unfiltered_microRNA_score' columns to 2 decimal places
    microRNA_score_table = microRNA_score_table.round({'filtered_microRNA_score': 2, 'unfiltered_microRNA_score': 2})
    
    # Define the desired column order for the output table
    column_order = ["species","analysis_node","filtered_total_count","filtered_microRNA_score","filtered_no_hits","unfiltered_total_count","unfiltered_microRNA_score","filtered_out_families"]
    
    # Reorder the columns in the dataframe based on the 'column_order' list
    microRNA_score_table = microRNA_score_table.reindex(columns=column_order)
    
    # Write the resulting dataframe to a tab-separated output file
    microRNA_score_table.to_csv(output_path, index=False)

    if json:
        # Write the resulting dataframe to a yaml file
        microRNA_score_table.to_json(output_path.split('.csv')[0] + '.json', orient='records', indent=4)

def main(args):

    # Read in the mirMachine heatmap file
    mammals_heatmap = parse_heatmap(args.input)

    # Read in the mirMachine metadata file
    if args.metadata:
        # This was the original code from Vanessa
        # I believe this is not optimal as it assumes all accessions are the same clade
        # new method should be run on each mirmachine output individually
        mirmachine_output_metadata = parse_metadata(args.metadata)
        # Extract tot families searched for
        mirmachine_total_families_searched = mirmachine_output_metadata.iloc[0][4]
    else:
        mirmachine_total_families_searched = get_mirmachine_total_families_searched(args.input)

    analysis_node = mammals_heatmap.iloc[1]['mode']

    # From the heatmap csv file, extract the species and the number of microRNA families that have been detected that met the bitscore threshold in mirMachine
    mammals_filtered_score = create_filtered_score_df(mammals_heatmap, mirmachine_total_families_searched)

    # From the heatmap csv file, extract the species and the number of microRNA families that have been detected that did not meet the bitscore threshold in mirMachine
    mammals_unfiltered_score = calculate_unfiltered_score(mammals_heatmap, mirmachine_total_families_searched)

    # microRNA families that have been filtered out
    family_ID = get_filtered_out_families(mammals_heatmap)

    # filtered families with 0 hits 
    mammals_filtered_missing = get_filtered_no_hits(mammals_heatmap)
    # Output the final table
    merge_and_output(mammals_filtered_score,
                        mammals_unfiltered_score,
                        analysis_node,
                        family_ID,
                        mammals_filtered_missing,
                        args.output,
                        args.json)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Score microRNA sequences')
    parser.add_argument('-i', '--input', type=str, help='Path to the mirMachine heatmap file')
    parser.add_argument('-m', '--metadata', required=False, type=str, help='DO NOT USE (should be removed soon): Path to the mirMachine metadata file')
    parser.add_argument('-o', '--output', type=str, help='Path to the mirMachine metadata file')
    parser.add_argument('--json', action='store_true', default=False, required=False, help='Ouput report as json file - Only works for single species input')
    args = parser.parse_args()

    main(args)