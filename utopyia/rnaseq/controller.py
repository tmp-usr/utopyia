import os

from aligner import Aligner


genome_dir1= "/proj/b2016253/nobackup/genomeDir"
genome_dir2= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/genomeDir"
genome_dir3= genome_dir2
genome_fasta_path= "/proj/b2016253/nobackup/GRCh38.d1.vd1.fa"

tmp_output_dir_1= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/tmp_1/"
tmp_output_dir_2= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/tmp_2/"

sjdb_file_chr_start_end= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/sj.out.tab"

sam_output= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/test.Aligned.sortedByCoord.out.bam"
gtf_output= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/test.gtf"
count_output= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/test.count"


test_data_base= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_data/"

fastq_1= os.path.join(test_data_base, "reads_1.fastq.gz")
fastq_2= os.path.join(test_data_base, "reads_2.fastq.gz")

fastq_pair= (fastq_1, fastq_2)

aln= Aligner(fastq_pair=fastq_pair, genome_dir1=genome_dir1, genome_dir2=genome_dir2, 
        genome_fasta_path=genome_fasta_path, sjdb_file_chr_start_end=sjdb_file_chr_start_end, 
        sam_out= sam_output, gtf_out=gtf_output, count_out= count_output, 
        tmp_output_dir_1= tmp_output_dir_1, tmp_output_dir_2= tmp_output_dir_2)

aln.align_fastq_pair()




