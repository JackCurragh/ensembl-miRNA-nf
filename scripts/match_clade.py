"""
Script that given a list of clades (e.g. from the NCBI taxonomy) and a species name (e.g. from the Ensembl API) will return the closest match

Usage:
    match_clade.py --clades <clades> --species <species> [--output <output>]

Options:
    --clades <clades>       Path to file containing list of clades (one per line)
    --species <species>     Species name    
    --output <output>       Output file [default: ./clade_match.txt]

Example:
    match_clade.py --clades clades.txt --species "Homo sapiens" --output clade_match.txt
"""

import argparse
from ete3 import NCBITaxa



def lint_args(args: argparse.Namespace) -> argparse.Namespace:
    """
    Lint arguments from argparse

    Parameters
    ----------
    args : argparse.Namespace
        Arguments from argparse

    Returns
    -------
    args : argparse.Namespace
        Arguments from argparse that have been linted
    """
    if args.species[0].islower():
        args.species = args.species.capitalize()

    if " " in args.species:
        args.species = args.species.replace(" ", "_")

    return args

def get_clade_match(clades: list, species_name: str) -> str:
    """
    Given a list of clades and a species name, return the closest match

    Parameters
    ----------
    clades : list
        List of clades
    species_name : str
        Species name

    Returns
    -------
    str
        Closest match
    """
    clade_match = []
    for clade in clades:
        if clade.lower() in species_name.lower():
            clade_match.append(clade)
    return clade_match[0]


def main(args: argparse.Namespace) -> None:
    """
    Main function

    Parameters
    ----------
    args : argparse.Namespace
        Arguments from argparse
    """
    with open(args.clades, "r") as file:
        clades = file.read().splitlines()
    
    clade_match = get_clade_match(clades, args.species)
    
    with open(args.output, "w+") as output:
        output.write(clade_match)

    get_clade_match(args.clades, args.species)

    return None

if __name__ == "__main__":
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
        help="Species name",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file",
        default="./clade_match.txt",
    )
    args = parser.parse_args()
    args = lint_args(args)
    main(args)
    
