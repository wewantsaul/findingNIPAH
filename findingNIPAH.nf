nextflow.enable.dsl=2

include {mainflow} from './workflows/mainflow.nf'
include {index} from './workflows/index.nf'

workflow {
	
	Channel
		.fromFilePairs("${params.reads}/*{,.trimmed}_{R1,R2,1,2}{,_001}.{fastq,fq}{,.gz}", flat:true)
		.ifEmpty{error "Cannot find any reads matching: ${params.reads}"}
		.set{ch_reads}

	main:
		
		if (params.index) {
			index(params.ref_seq)
		}
		else {
			mainflow(ch_reads)
		}
		
}	
