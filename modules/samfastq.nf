process samfastq {
	container 'staphb/samtools:1.18'

	tag "extracting fastq pairs from filtered $sample"

	publishDir (
	path: "${params.out_dir}/$sample/03_filteredfastq/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(filtered_bam)

	output:
	tuple val(sample), path("*1.fastq.gz"), path("*2.fastq.gz"), emit: filtered_fastq
	tuple val(sample), path("*singletons.fastq.gz")

	script:
	"""
	samtools fastq -1 ${sample}_filtered_1.fastq.gz \
	-2 ${sample}_filtered_2.fastq.gz \
	-0 /dev/null -s ${sample}_singletons.fastq.gz \
	-n $filtered_bam
	"""
}
