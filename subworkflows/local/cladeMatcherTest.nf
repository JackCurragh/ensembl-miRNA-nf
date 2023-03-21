include { LIST_MIRMACHINE_CLADES; FORMAT_CLADES; MATCH_CLADE } from '../../modules/local/clade_matcher.nf'
include { RAPID } from '../../modules/local/rapid.nf'


process CAT_TO_FILE {
    publishDir "${params.outdir}/clade_assignment_test", mode: 'copy'

    input:
        val clade
        val species
        val accession


    output:
        file "formatted_clades.txt"

    script:
        """
        echo "${species},${accession},${clade} >> $projectDir/data/clade_assignments.txt
        """
}


workflow cladeTest {

    take:
        species
        accession
        mirMachine_clades

    main:
        mirMachine_clades_ch    =   Channel.fromPath(mirMachine_clades)
        fasta_ch                =   RAPID(species, accession)
        formatted_clades_ch     =   FORMAT_CLADES(mirMachine_clades_ch)
        match_ch                =   MATCH_CLADE(species, accession, formatted_clades_ch)
        CAT_TO_FILE(match_ch, species, accession)

}

workflow {
    
    cladeTest(params.species, params.accession, params.mirMachine_clades)
}