
include { mirMachine } from './subworkflows/local/mirMachine.nf'

log.info """\

    m i R N A    N F    P I P E L I N E
    =========================================
    species: ${params.species}
    accession: ${params.accession}
    =========================================
"""



workflow {

    mirMachine(params.species, params.accession)
}
