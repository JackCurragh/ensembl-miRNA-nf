
include { RAPID } from '../../modules/local/rapid.nf'
include { LIST_MIRMACHINE_CLADES; FORMAT_CLADES; MATCH_CLADE } from '../../modules/local/mirMachine_node_matcher.nf'


workflow mirMachine {

    take:
        species
        accession
        mirMachine_clades

    main:
        mirMachine_clades_ch    =   Channel.fromPath(mirMachine_clades)
        mirMachine_clades_ch.view()
        fasta_ch                =   RAPID(species, accession)
        // clades_ch               =   LIST_MIRMACHINE_CLADES()
        formatted_clades_ch     =   FORMAT_CLADES(mirMachine_clades_ch)
        match_ch                =   MATCH_CLADE(species, accession, formatted_clades_ch)
    
    emit:
        fasta_ch
}