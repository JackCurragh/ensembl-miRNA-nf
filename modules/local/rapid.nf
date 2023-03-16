

process RAPID {

    input:
        val(species)
        val(accession)

    output:
        file "*.fa"

    script:
        """
        python $projectDir/scripts/rapid_fetch.py -s '${species}' -a '${accession}'
        gzip -d *.gz
        """

}