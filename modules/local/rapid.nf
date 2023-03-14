

process RAPID {

    input:
        val species
        val accession

    output:
        file "*.fa.gz"

    script:
        """
        python $projectDir/scripts/rapid_fetch.py -s $species -a $accession 
        """

}