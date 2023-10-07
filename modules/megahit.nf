process megahit {
	container 'nanozoo/megahit:1.2.9--87c4487'

	tag "assembling contigs from $sample reads"

	publishDir (
	path: "${params.out_dir}/$sample/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(fastq_1), path(fastq_2)

	output:
	tuple val(sample), path("04_assembly/*.contigs.fa"), emit: consensus

	script:
	"""
	megahit -1 ${sample}*_1.fastq.gz -2 ${sample}*_2.fastq.gz --out-prefix $sample -o 04_assembly
	"""
}

