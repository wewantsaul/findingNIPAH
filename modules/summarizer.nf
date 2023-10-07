process summarizer {
	container 'python:3.8-bullseye'

	tag "summarizing results"

	publishDir (
	path: "${params.out_dir}/$sample/06_final_results/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(blast_nuc)
	tuple val(sample), path(blast_prot)

	output:
	tuple val(sample), path("*blastn_report.html")
	tuple val(sample), path("*blastx_report.html")
	tuple val(sample), path("*summary_report.html")
	tuple val(sample), path("*summary_report.txt"), emit: sum_report

	script:
	"""
	htmlgenerator.py --blast_type blastn --input $blast_nuc --output ${sample}_blastn_report.html
	
	htmlgenerator.py --blast_type blastx --input $blast_prot --output ${sample}_blastx_report.html
	
	summarizer.py --blastn $blast_nuc --blastx $blast_prot --output_html ${sample}_summary_report.html --output_txt ${sample}_summary_report.txt
	"""
}