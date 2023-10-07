process bamstats {
	container 'staphb/samtools:1.18'

	tag "determining bam alignment stats from $sample"

	publishDir (
	path: "${params.out_dir}/$sample/02_alignment/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(aligned_bam)

	output:
	tuple val(sample), path("*.flagstats.txt")

	script:
	"""
	samtools flagstats $aligned_bam > ${sample}_aligned_bam.flagstats.txt
	"""
}