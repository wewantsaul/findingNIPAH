process blastn {
	container 'staphb/blast:2.14.0'

	tag "comparing sequences from NIPAH database"

	publishDir (
	path: "${params.out_dir}/$sample/05_blast/",
	mode: 'copy',
	overwrite: 'true'
	)
	
	input:
	// tuple val(sample), path(singletons_fa)
	tuple val(sample), path(consensus)

	output:
	// tuple val(sample), path("*allseq.fa"), emit: allseq
	tuple val(sample), path("*blastn_results.txt"), emit: blast_nuc

	script:
	
	// cat $singletons_fa $consensus > ${sample}_allseq.fa
	
	"""
	blastn -query $consensus \
	-db $PWD/database/nipah_nuc_db/nipahdb \
	-out ${sample}_blastn_results.txt \
	-outfmt "6 qseqid sseqid stitle pident qlen length qstart qend sstart send evalue bitscore qseq sseq"
	"""
}
