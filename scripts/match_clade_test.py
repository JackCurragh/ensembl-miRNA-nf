'''
This script runs match clade for all species in ensembl rapid and produces a table of the results

The table is saved as a csv file in the projects data directory 

Usage:
    match_clade_test.py --clades <clades> --species <species_csv> [--output <output>]

Options:
    --clades <clades>       Path to file containing list of clades (one per line)
    --species <species_csv> Path to csv file containing species names downloaded from the ensembl rapid website
    --output <output>       Output file [default: ./clade_match.txt]

'''

from match_clade import get_clade_match, get_ncbi, get_taxid, taxoniq_match
import pandas as pd
import ete3
from ete3 import NCBITaxa



def main(args):
    with open(args.clades, "r") as file:
        clades = [line[:max(line.find(' '), 0) or None] for line in file]

    species = pd.read_csv(args.species, header=0)

    ncbi = get_ncbi()
    results = []
    for idx, row in species.iterrows():
        if row['Clade'] == "Plants":
            continue
        species_name = row['Scientific name'].split(" ")[0] + " " + row['Scientific name'].split(" ")[1]
        try:
            match = get_clade_match(ncbi, clades, species_name)[0]
        except Exception as e:
            if str(e) == "list index out of range":
                match = 'Taxid finding issue'
            elif str(e) == "No match found":
                match = 'No match found'
            else:
                raise e

        try:
            taxid = get_taxid(ncbi, species_name)
            tx_match = taxoniq_match(species_name, taxid, clades)[0]
        except Exception as e:
            if str(e) == "list index out of range":
                tx_match = 'Taxid finding issue'
            elif str(e) == "No match found":
                tx_match = 'No match found'
            elif str(e) == "'KeyError' object is not subscriptable":
                tx_match = 'Taxid finding issue'
            else:
                raise e
        results.append([species_name, match, tx_match])


    df = pd.DataFrame(results, columns=['species', 'ete3_clade', 'taxoniq_clade'])
    df.to_csv(args.output, index=False)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--clades",
        type=str,
        help="Path to file containing list of clades (one per line)",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--species",
        type=str,
        help="Path to csv file containing species names downloaded from the ensembl rapid website",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file",
        default="./clade_match.txt",
    )
    args = parser.parse_args()
    main(args)