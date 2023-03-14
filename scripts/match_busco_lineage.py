#!/usr/bin/env python

import argparse
import difflib
import os
from ete3 import NCBITaxa
  
def get_busco_lineage(ncbi,species_name: str, busco_lineages: list)->str:
  # get taxonomy id
  name2taxid = ncbi.get_name_translator([species_name])
  taxon_id=str(list(name2taxid.values())[0]).strip("[]")
  # get entire taxonomy ids
  lineage=ncbi.get_lineage(taxon_id)
  # get species name
  names = ncbi.get_taxid_translator(lineage)
  lineage_list=list([names[taxid] for taxid in lineage])
  
  # from lower level of the taxonomy find the closest match with busco lineages
  busco_match=[]
  for i in reversed(lineage_list):
    for l in busco_lineages:
      if l.startswith(str(i[:len(i)-2].lower())):
        busco_match.append(l)
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

    ncbi = NCBITaxa()
    ncbi.update_taxonomy_database()
  
    get_busco_lineage(ncbi,species_name, busco_lineages)