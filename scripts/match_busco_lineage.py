#!/usr/bin/env python

import argparse
import difflib
import os
from ete3 import NCBITaxa
import taxoniq

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
    
def taxoniq_match(taxid: int = 9606, busco_lineages: list = None):
    t = taxoniq.Taxon(taxid)
    lineage = [t.scientific_name for t in t.ranked_lineage]
    if not check_lineage_order(t.scientific_name, lineage):
       lineage = lineage[::-1]

    if busco_lineages is None:
       raise ValueError("busco_lineages must be provided")
    
    busco_match = []
    for i in reversed(lineage):
        for l in busco_lineages:
            if l.strip().lower() == i.strip().lower():
                busco_match.append(l.strip())
            elif l.strip().startswith(str(i.strip()[:len(i)-2].lower())):
                busco_match.append(l)
    print(busco_match)
    return busco_match[0]
  
def get_busco_lineage(ncbi,species_name: str, busco_lineages: list)->str:
  # get taxonomy id
  name2taxid = ncbi.get_name_translator([species_name])
  taxon_id=str(list(name2taxid.values())[0]).strip("[]")
  print(species_name, taxon_id)
  # get entire taxonomy ids
  lineage=ncbi.get_lineage(taxon_id)
  # get species name
  names = ncbi.get_taxid_translator(lineage)
  lineage_list=list([names[taxid] for taxid in lineage])
  
  # from lower level of the taxonomy find the closest match with busco lineages
  busco_match=[]
  print(lineage_list)
  print(busco_lineages)
  for i in reversed(lineage_list):
    for l in busco_lineages:
    #   print(i[:len(i)-2].lower(), l, l.strip().startswith(str(i[:len(i)-2].lower())))
      if l.strip().startswith(str(i[:len(i)-2].lower())):
        busco_match.append(l)
  print(busco_match)
  with open('./lineage_match.txt',"w+") as lineage:
    lineage.write(str(busco_match[0]))
  return busco_match[0]

if __name__ == "__main__":
     
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--busco_lineages",
        type=str,
        help="List of Busco lineages",
    )
    parser.add_argument(
        "--species_name",
        type=str,
        help="Species name",
        required=True, 
    )
    args = parser.parse_args()
    
    species_name = args.species_name
    
    if args.busco_lineages:
        with open(args.busco_lineages, "r") as file:
            busco_lineages = file.read().splitlines()
        
    else:
        with open('/ncbi_taxa/busco_dataset.txt', "r") as file:
            busco_lineages = file.read().splitlines()

    # taxoniq_match(busco_lineages=busco_lineages)
    ncbi = NCBITaxa()
    # ncbi.update_taxonomy_database()
  
    get_busco_lineage(ncbi,species_name, busco_lineages)