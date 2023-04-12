
include { RAPID } from '../../modules/local/rapid.nf'
include { LIST_MIRMACHINE_CLADES; FORMAT_CLADES; MATCH_CLADE } from '../../modules/local/clade_matcher.nf'
include { MIRMACHINE } from '../../modules/local/mirMachine.nf'

workflow mirMachine {

    take:
        species
        accession

    main:
        fasta_ch                =   RAPID(species, accession)
        clades_ch               =   LIST_MIRMACHINE_CLADES()
        formatted_clades_ch     =   FORMAT_CLADES(clades_ch)
        match_ch                =   MATCH_CLADE(species, accession, formatted_clades_ch)
        match_ch.view()
        clean_species = species.replaceAll(~/\s/,"")
        MIRMACHINE(clean_species, match_ch, fasta_ch)
    
    emit:
        fasta_ch
}