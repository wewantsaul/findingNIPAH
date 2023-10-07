process fastp {
	container 'staphb/fastp:0.23.4'

	tag "trimming $sample"

	publishDir (
	path: "${params.out_dir}/$sample/01_fastp/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	//errorStrategy 'ignore'
	
	input:
	tuple val(sample), path(fastq_1), path(fastq_2)

	output:
	tuple val(sample), path("*1.fastq.gz"), path("*2.fastq.gz"), emit: trimmed
	tuple val(sample), path("*.json"), emit: fastp_json
	tuple val(sample), path("*.html"), emit: fastp_html

	script:
	"""
	fastp -i $fastq_1 \
	-I $fastq_2 \
	-o ${sample}.trimmed_R1.fastq.gz \
	-O ${sample}.trimmed_R2.fastq.gz \
	-j ${sample}.fastp.json \
	-h ${sample}.fastp.html
	"""
}
