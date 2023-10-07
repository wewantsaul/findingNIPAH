nextflow.enable.dsl=2

include {fastp} from '../modules/fastp.nf'
include {bwamem} from '../modules/bwamem.nf'
include {bamstats} from '../modules/bamstats.nf'
include {samfilter} from '../modules/samfilter.nf'
include {samfastq} from '../modules/samfastq.nf'
include {megahit} from '../modules/megahit.nf'
// include {singletons} from '../modules/singletons.nf'
include {blastn} from '../modules/blastn.nf'
include {blastx} from '../modules/blastx.nf'
include {summarizer} from '../modules/summarizer.nf'
include {combinesummary} from '../modules/combinesummary.nf'

workflow mainflow {

	take:
		ch_reads

	main:
		fastp(ch_reads)
		bwamem(fastp.out.trimmed)
		bamstats(bwamem.out.aligned_bam)
		samfilter(bwamem.out.aligned_bam)
		samfastq(samfilter.out.filtered_bam)
		megahit(samfastq.out.filtered_fastq)
		// singletons(samfastq.out.singletons_fastq)
		blastn(megahit.out.consensus)
		// blastn(singletons.out.singletons_fa, megahit.out.consensus)
		blastx(megahit.out.consensus)
		summarizer(blastn.out.blast_nuc, blastx.out.blast_prot)
		combinesummary(summarizer.out.sum_report)
}	

