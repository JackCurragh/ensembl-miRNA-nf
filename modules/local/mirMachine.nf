
process MIRMACHINE {
    container "${params.container}"
    publishDir "${params.outdir}/mirmachine", mode: 'copy'
    
    input:
        val(species)
        val(node)
        file fasta

    output:
        path "*"

    script:
        """
        MirMachine.py --cpu ${task.cpus} --node ${node} --species  "${species}" --genome ${fasta} > log_file 2>> err_file
        """

}