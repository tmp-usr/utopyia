def kallisto_run(genome_index, output_dir, fastq_pair):
    """
kallisto inputs differ from star. kallisto requires a pregenerated index file as input.
@kallisto_genome_index
@fastq_pair
@sample_id
@output_dir
@
    """    
    command_line= """
#loading kallisto library
module load kallisto/0.43.0

kallisto quant -i %s -o %s -t 16 %s %s
"""
%(genome_index, output_dir, fastq_pair.reads_1, fastq_pair.reads_2)
