nextflow.enable.dsl = 2

include { mirMachine } from './subworkflows/local/mirMachine.nf'

log.info """\

    m i R N A    N F    P I P E L I N E
    =========================================
    species: ${params.species}
    accession: ${params.accession}
    mirMachine_clades: ${params.mirMachine_clades}
    =========================================
"""



workflow {
    inputs = Channel
        .fromPath(params.csv)
        .splitCsv(header: true)
        .map { row -> tuple("${row.Accession}", "${row.SRA}" )} // use for superset  

    main:
        mirMachine(params.species, params.accession, params.mirMachine_clades)
}
