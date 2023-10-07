process combinesummary {
	container 'python:3.8-bullseye'

	tag "combining summary results"

	publishDir (
	path: "${params.out_dir}",
	mode: 'copy',
	overwrite: 'true'
	)
	input:
	tuple val(sample), path(sum_report)

	output:
	path "*.html"
	path "*.txt"
	

	script:
	"""
	CombineSummary.py --input_folder $PWD/$params.out_dir --output_html summary_report.html --output_txt summary_report.txt
	"""
}