process samfilter {
	container 'staphb/samtools:1.18'

	tag "filtering reference sequence from $sample"

	publishDir (
	path: "${params.out_dir}/$sample/02_alignment/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(aligned_bam)

	output:
	tuple val(sample), path("*filtered.bam"), emit: filtered_bam

	script:
	"""
	samtools view -f 4 -h $aligned_bam | samtools sort -n -o ${sample}_filtered.bam
	"""
}
