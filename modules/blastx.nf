process blastx {
	container 'nanozoo/diamond:2.0.9--3b48005'

	tag "blastx"

	publishDir (
	path: "${params.out_dir}/$sample/05_blast/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	tuple val(sample), path(consensus)

	output:
	tuple val(sample), path("*blastx_results.txt"), emit: blast_prot

	script:
	"""
	diamond blastx \
	-d $PWD/database/nipah_prot_db/reference.dmnd \
	-q $consensus -o ${sample}_blastx_results.txt \
	-f 6 qseqid sseqid stitle pident qlen length qstart qend sstart send evalue bitscore qseq sseq
	"""
}
