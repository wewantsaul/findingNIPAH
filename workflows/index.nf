nextflow.enable.dsl=2

include {bwaindex} from '../modules/bwaindex.nf'

workflow index {

	take:
	
		reference_sequence
	
	main:
	
		bwaindex(reference_sequence)
}