process EC_COMBINE {
    label 'process_single'

    container "docker.io/systemsgenetics/annotater:1.0.0-dev"

    input:
    path ecfiles
    val sequence_filename

    output:
    path ("${sequence_filename}_EC_mappings.txt"), emit: outfile
    path ("versions.yml"), emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    """
    combine_ec.sh "${sequence_filename}_EC_mappings.txt"

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        combine_ec.sh: AnnoTater ${workflow.manifest.version}
    END_VERSIONS
    """
}