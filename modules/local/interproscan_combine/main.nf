process INTERPROSCAN_COMBINE {
    label 'process_single'

    container "docker.io/systemsgenetics/annotater:1.0.0-dev"

    input:
    path tsv_files
    val sequence_filename

    output:
    path "${sequence_filename}.IPR_mappings.txt", emit: ipr_mappings
    path "${sequence_filename}.GO_mappings.txt", emit: go_mappings
    path "${sequence_filename}.tsv", emit: tsv
    path "versions.yml", emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    """
    interpro_combine.py ${sequence_filename}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        interpro_combine.py: AnnoTater ${workflow.manifest.version}
    END_VERSIONS
    """
}
