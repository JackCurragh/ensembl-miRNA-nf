
process MIRMACHINE {

    container = 'singularity/mirmachine%3A0.2.12--pyhdfd78af_0'

    publishDir "${params.outdir}/mirmachine", mode: 'copy'

    cpus 4
    
    input:
        val(species)
        val(node)
        file fasta

    output:
        file "*.fa*"
        file "*/*.gff*"

    script:
        """
        MirMachine.py --cpu ${task.cpus} --node ${node} --species  "${species}" --genome ${fasta}
        """

}