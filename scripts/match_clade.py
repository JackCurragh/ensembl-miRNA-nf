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
import ete3
from ete3 import NCBITaxa
try:
    import taxoniq
except ImportError:
    pass


def check_lineage_order(species: str, lineage: list) -> bool:
    """
    Return True if the lineage is in the correct order (from higher to lower)

    Parameters
    ----------
    lineage : list
        List of lineages

    Returns
    -------
    bool
        True if the lineage is in the correct order (from higher to lower)
    """
    if lineage[-1] == species:
        return True
    else:
        return False


def taxoniq_match(species: str, taxid: int, tool_lineage: list) -> str:
    """
    Check for a suitable match using taxoniq

    Parameters
    ----------
    species : str
        Species name
    taxid : int
        Taxonomy ID
    tool_lineage : list
        List of lineages

    Returns
    -------
    str
        Closest match
    """
    try:
        t = taxoniq.Taxon(taxid)
    except Exception as e:
        return e
    lineage = [t.scientific_name for t in t.ranked_lineage]
    if not check_lineage_order(t.scientific_name, lineage):
        lineage = lineage[::-1]

    if tool_lineage is None:
        raise ValueError("Tool lineages must be provided")

    matches = []
    for i in reversed(lineage):
        for l in tool_lineage:
            if l.strip().lower() == i.strip().lower():
                matches.append(l.strip())
            elif l.strip().startswith(str(i.strip()[: len(i) - 2].lower())):
                matches.append(l)
    return matches


def ete3_match(ncbi: ete3.ncbi_taxonomy.ncbiquery.NCBITaxa, species: str, tool_lineage: list) -> str:
    """
    Check for a suitable match using ete3

    Parameters
    ----------
    ncbi : ete3.ncbi_taxonomy.ncbiquery.NCBITaxa
        Instance of ete3.ncbi_taxonomy.ncbiquery.NCBITaxa
    species : str
        Species name
    tool_lineage : list
        List of lineages

    Returns
    -------
    str
        Closest match
    """

    taxon_id = get_taxid(ncbi, species)
    lineage = ncbi.get_lineage(taxon_id)
    names = ncbi.get_taxid_translator(lineage)
    lineage_list = [names[taxid] for taxid in lineage]
    if not check_lineage_order(species, lineage_list):
        lineage_list = lineage_list[::-1]

    match = []
    for i in reversed(lineage_list):
        for l in tool_lineage:
            if l.strip().lower() == i.strip().lower():
                match.append(l.strip())
            elif l.strip().startswith(str(i[: len(i) - 2].lower())):
                match.append(l)

    return match

def get_ncbi(update: bool = False) -> ete3.ncbi_taxonomy.ncbiquery.NCBITaxa:
    """
    Get an instance of ete3.ncbi_taxonomy.ncbiquery.NCBITaxa

    Parameters
    ----------
    update : bool
        Update the NCBI taxonomy database

    Returns
    -------
    ete3.ncbi_taxonomy.ncbiquery.NCBITaxa
        Instance of ete3.ncbi_taxonomy.ncbiquery.NCBITaxa
    """
    ncbi = NCBITaxa()
    if update:
        ncbi.update_taxonomy_database()
    return ncbi

def get_taxid(ncbi: ete3.ncbi_taxonomy.ncbiquery.NCBITaxa, species_name: str) -> int:
    """
    Given a species name, return the taxonomy ID

    Parameters
    ----------
    species_name : str
        Species name

    Returns
    -------
    int
        Taxonomy ID
    """
    try:
        name2taxid = ncbi.get_name_translator([species_name])
        taxon_id = str(list(name2taxid.values())[0]).strip("[]")
        return taxon_id
    except IndexError:
        ncbi = get_ncbi(update=True)
        name2taxid = ncbi.get_name_translator([species_name])
        taxon_id = str(list(name2taxid.values())[0]).strip("[]")
        return taxon_id
    except:
        raise ValueError("Species name not found")

    

def get_clade_match(ncbi: ete3.ncbi_taxonomy.ncbiquery.NCBITaxa, clades: list, species_name: str) -> str:
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
    species_name = ' '.join(species_name.split(" ")[:2])
    if not check_lineage_order(species_name, clades):
        clades = clades[::-1]
    return ete3_match(ncbi, species_name, clades)


def main(args: argparse.Namespace) -> None:
    """
    Main function

    Parameters
    ----------
    args : argparse.Namespace
        Arguments from argparse
    """
    with open(args.clades, "r") as file:
        clades = [line[:max(line.find(' '), 0) or None] for line in file]
        
    ncbi = get_ncbi()
    clade_match = get_clade_match(ncbi, clades, args.species)

    if clade_match == []:
        raise ValueError("No match found")
    
    if args.output == "stdout":
        if clade_match[0] == args.species:
            print(clade_match[1].strip('\n'), end='')
            return None
        else:
            print(clade_match[0].strip('\n'), end='')
            return None
    else:
        with open(args.output, "w+") as output:
            if clade_match[0] == args.species:
                output.write(clade_match[1])
            else:
                output.write(clade_match[0])

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
    parser.add_argument("-s", "--species", type=str, help="Species name", required=True)
    parser.add_argument(
        "--output", type=str, help="Output file", default="./clade_match.txt"
    )
    args = parser.parse_args()
    main(args)
