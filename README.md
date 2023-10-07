# findingNIPAH
The findingNIPAH pipeline is a Nextflow-based tool designed for detecting the NIPAH virus in animal samples, such as bat urine and feces, using Illumina paired-end metagenomic sequencing data.

## Pipeline details
Host genome indexing. \
Quality control using fastp. \
Alignment to the host genome using bwa. \
Host sequence filtering and extraction of paired-end FASTQ files using samtools. \
Contig assembly using megahit. \
BLASTN and BLASTX searches against NIPAH virus-related databases.

## Installation and Requirements
* clone repository
```
git clone https://github.com/wewantsaul/findingNIPAH.git
```
* create nextflow environment and install nextflow \
```conda create -n nextflow-env``` \
```conda activate nextflow-env``` \
```conda install nextflow```
* install docker \
see [here](https://docs.docker.com/engine/install/)
* get host genome

## Usage
Before proceeding, set the clone as the working directory
```
cd ~/findingNIPAH
```
### Step 1: Indexing
```
nextflow run findingNIPAH --index \
--ref_seq <path/to/reference_fasta.fna> \
--index_dir <NAME_of_index_directory>
```
* <path/to/reference_fasta.fna>: Provide the path to the host reference genome in .fna format
* <NAME_of_index_directory>: Specify the name of the index directory (not the path)
### Step 2: Main Workflow
```
nextflow run findingNIPAH --reads <path/to/fastq> \
--out_dir <output_directory_NAME> \
--index_folder <index_folder_NAME>
```
* <path/to/fastq>: Provide the path to the input FASTQ files.
* <output_directory_NAME>: Specify the name of the output directory (not the path).
* <index_folder_NAME>: Specify the name of the index folder (not the path).
  
## Detection Critera
The pipeline uses the following detection criteria for NIPAH virus:
* BLAST alignment of >100 nt/aa
* E-value < 0.00001 or bit score > 100





