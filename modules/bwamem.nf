process bwamem {
	container 'biocontainers/bwa:v0.7.17_cv1'

	tag "aligning $sample to reference"

	publishDir (
	path: "${params.out_dir}/$sample/02_alignment/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(fastq_1), path(fastq_2)

	output:
	tuple val(sample), path("*aligned.bam"), emit: aligned_bam

	script:
	"""
	bwa mem -t 4 \
	$PWD/$params.index_folder/*.fna \
	$fastq_1 $fastq_2 > ${sample}_aligned.bam
	"""
}
