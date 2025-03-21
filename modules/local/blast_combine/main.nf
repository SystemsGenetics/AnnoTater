process BLAST_COMBINE {
    label 'process_single'

    container "docker.io/systemsgenetics/annotater:1.0.0-dev"

    input:
    path outfiles
    val blast_type
    val sequence_filename
    val db_name

    output:
    path ("${blast_type}_${sequence_filename}_${db_name}.out"), emit: outfile
    path ("versions.yml"), emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    """
    combine_blast.sh "${blast_type}_${sequence_filename}_${db_name}.out"

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        interpro_combine.py: AnnoTater ${workflow.manifest.version}
    END_VERSIONS
    """
}
