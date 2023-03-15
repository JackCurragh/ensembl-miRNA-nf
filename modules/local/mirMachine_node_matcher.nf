
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
        file "clades.txt"

    shell:
        """ 
#!/usr/bin/env python
with open("clades.txt", "w") as outfile:

    with open("${clades}", "r") as f:
        clades = f.readlines()
        clades_list = []
        for line in clades:
            print(line)
            for clade in line.split(" "):
                outfile.write(f"{clade.strip()}")
        """

}

process MATCH_CLADE {

    input:
        val(species)
        val(accession)
        file clade_file

    output:
        val(stdout)

    script:
        """
        python $projectDir/scripts/match_clade.py -s "${species}" -c $clade_file
        """

}