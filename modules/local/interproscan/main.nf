process INTERPROSCAN {
    tag "$meta.id"
    label 'process_medium'
    label 'process_long'

    conda "${moduleDir}/environment.yml"
    container "docker.io/interpro/interproscan:5.75-106.0"
    containerOptions { workflow.containerEngine == 'docker' ? "--entrypoint=''" : '' }

    input:
    tuple val(meta), path(fasta)
    path(interproscan_database, stageAs: 'data')

    output:
    tuple val(meta), path('*.tsv') , optional: true, emit: tsv
    tuple val(meta), path('*.xml') , optional: true, emit: xml
    tuple val(meta), path('*.gff3'), optional: true, emit: gff3
    tuple val(meta), path('*.json'), optional: true, emit: json
    path "versions.yml"            , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    def is_compressed = fasta.name.endsWith(".gz")
    def fasta_name = fasta.name.replace(".gz", "")
    """
    # Create temp directory
    mkdir -p temp

    # Add interproscan to PATH for Singularity compatibility
    export PATH="\$PATH:/opt/interproscan"

    # Link the database to expected location (works in both Docker and Singularity)
    if [ -d "data" ]; then
        export INTERPROSCAN_DATA_DIR=\$PWD/data
    fi

    # Handle compressed input
    if ${is_compressed} ; then
        gzip -c -d ${fasta} > ${fasta_name}
    fi

    # Run InterProScan - works with both Docker and Singularity
    interproscan.sh \\
        --input ${fasta_name} \\
        --tempdir \$PWD/temp \\
        --cpu ${task.cpus} \\
        ${args} \\
        --output-file-base ${prefix}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        interproscan: \$( interproscan.sh --version | sed '1!d; s/.*version //' )
    END_VERSIONS
    """

    stub:
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    touch ${prefix}.{tsv,xml,json,gff3}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        interproscan: \$( interproscan.sh --version | sed '1!d; s/.*version //' )
    END_VERSIONS
    """
}
