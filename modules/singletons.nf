process singletons {
	container 'nanozoo/seqtk:1.3--dc0d16b'

	tag "extracting fasta sequences from $sample singletons fastq"

	publishDir (
	path: "${params.out_dir}/$sample/04_assembly/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(singletons_fastq)

	output:
	tuple val(sample), path("*singletons.fa"), emit: singletons_fa

	script:
	"""
	seqtk seq -A $singletons_fastq > ${sample}_singletons.fa
	
	"""
}
