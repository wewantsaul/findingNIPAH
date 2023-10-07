process bwaindex {
	container 'biocontainers/bwa:v0.7.17_cv1'
	
	tag "indexing ${params.ref_seq}"

	publishDir (
	path: "$PWD",
	mode: 'copy',
	overwrite: 'true'
	)

	input:
	path(ref_seq)
	
    output:
    path("${params.index_dir}/*.{fasta,fa,fna}*")

  script:
    """
	mkdir -p ${params.index_dir} \
	
	cp ${params.ref_seq} ${params.index_dir}
	
	bwa index ./${params.index_dir}/*
    """
}