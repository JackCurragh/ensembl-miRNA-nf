'''
Fetch assembly FASTA file from ensembl Rapid release

Usage:
    rapid_fetch.py -s <species> -a <assembly GCA> -o <output>

Options:
    -s <species>        Species name
    -a <assembly GCA>   Assembly GCA
    -o <output>         Output file

Example:
    rapid_fetch.py -s 'Homo sapiens' -a GCA_000001405.15 -o GCA_000001405.15.fasta

'''

import argparse
import requests


def lint_args(args: argparse.Namespace) -> argparse.Namespace:
    '''
    Lint arguments from argparse
    
    Parameters
    ----------
    args : argparse.Namespace
        Arguments from argparse
    
    Returns
    -------
    args : argparse.Namespace
        Arguments from argparse that have been linted
    '''
    if args.species[0].islower():
        args.species = args.species.capitalize()
    
    if " " in args.species:
        args.species = args.species.replace(" ", "_")

    args.assembly = args.assembly.upper()
    
    return args


def check_url_validity(url: str) -> bool:
    '''
    Assess whether an ensemble URL is valid

    Parameters
    ----------
    url : str
        URL to check

    Returns
    -------
    bool
        Whether the URL is valid
    '''
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False


def build_url(species: str, assembly: str, annotation_types=['ensembl', 'refseq', 'braker', 'community', 'genbank', 'flybase', 'wormbase', 'noninsdc']) -> str:
    '''
    Build ensembl Rapid release URL from species name and assembly GCA
    
    Parameters
    ----------
    species : str
        Species name
    assembly : str
        Assembly GCA
    
    Returns
    -------
    str
        Ensembl Rapid release URL
    '''
    base_url = f"https://ftp.ensembl.org/pub/rapid-release/species/{species}/{assembly}"

    tested_urls = [] 
    for annotation_type in annotation_types:
        tested_urls.append(f"{base_url}/{annotation_type}/genome/{species}-{assembly}-softmasked.fa.gz")
        if check_url_validity(f"{base_url}/{annotation_type}"):
            return f"{base_url}/{annotation_type}/genome/{species}-{assembly}-softmasked.fa.gz"
    else:
        raise ValueError(f"Could not find assembly {assembly} for species {species} in ensembl Rapid release. Tested {tested_urls}")


def fetch_fasta(url: str, output: str):
    '''
    Fetch FASTA file from ensembl Rapid release URL

    Parameters
    ----------
    url : str
        URL to fetch FASTA file from
    output : str
        Output file

    Returns
    -------
    None
    '''
    fasta = requests.get(url).content
    open(output, "wb").write(fasta)


def main(args: argparse.Namespace):
    '''
    Main funciton to fetch assembly FASTA file from ensembl Rapid release
    
    Parameters
    ----------
    args : argparse.Namespace
        Arguments from argparse
    
    Returns
    -------
    None
    '''
    args = lint_args(args)
    url = build_url(args.species, args.assembly)
    output = f"{args.output}/{args.assembly}.fa.gz"
    fetch_fasta(url, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--species",
        type=str,
        help="Species name (preferably of the form 'Homo sapiens')",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--assembly",
        type=str,
        help="Assembly GCA (preferably of the form 'GCA_000001405.15')",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output direcotry",
        default=".",
    )
    args = parser.parse_args()
    main(args)