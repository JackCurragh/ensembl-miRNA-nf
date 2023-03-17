
process LIST_MIRMACHINE_CLADES {
    
    output:
        path "*txt"

    script:
        """
        MirMachine.py --print-all-nodes > clades.txt
        """
    
}


process FORMAT_CLADES {

    input:
        file clades

    output:
        file "formatted_clades.txt"

    shell:
        """ 
#!/usr/bin/env python
with open("formatted_clades.txt", "w") as outfile:

    with open("${clades}", "r") as f:
        clades = f.readlines()
        clades_list = []
        for line in clades[1:]:
            for clade in line.split(" "):
                outfile.write(f"{clade.strip()}")
                outfile.write("\\n")
        """

}

process MATCH_CLADE {
    // conda 'conda/match_clade.yaml'

    input:
        val(species)
        val(accession)
        file clade_file

    output:
        stdout

    script:
        """
        /home/jack/projects/ensembl-miRNA-nf/work/conda/clade_matcher-ba96d969ccb22b7830be38e274811851/bin/python $projectDir/scripts/match_clade.py -s "${species}" -c $clade_file --output stdout
        """

}