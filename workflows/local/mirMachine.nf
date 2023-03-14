
INCLUDE { RAPID } from '../modules/local/rapid.nf'


workflow mirMachine {
    RAPID(params.species, params.accession)
}