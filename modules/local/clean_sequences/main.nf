process CLEAN_SEQUENCES {
    tag "$meta.id"
    label 'process_single'

    container "docker.io/systemsgenetics/annotater:1.0.0-dev"

    input:
    tuple val(meta), path(fasta)
    val seq_type

    output:
    tuple val(meta), path("*_cleaned.fasta"), emit: fasta
    path ("versions.yml"), emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def prefix = task.ext.prefix ?: "${meta.id}"
    def fasta_name = fasta.getBaseName()
    """
    clean_sequences.py \\
        --input ${fasta} \\
        --output ${fasta_name}_cleaned.fasta \\
        --seq_type ${seq_type}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        clean_sequences.py: AnnoTater ${workflow.manifest.version}
    END_VERSIONS
    """
}