import os
import shutil

from aligner import Aligner
from project.project import Project
from config.file_provider import RNASeqIOProvider

import time


op= RNASeqIOProvider()
input_root_dir= op.input_root_dir

#### tmp
tmp_output_dir_1=  op.tmp_provider.tmp_output_dir_1.path
tmp_output_dir_2=   op.tmp_provider.tmp_output_dir_2.path
merge_split_dir= op.tmp_provider.merge_split_dir.path

#### reference
genome_dir1= op.ref_provider.ref_genome_dir.path
genome_dir2= op.tmp_provider.reindexed_genome_dir.path
genome_fasta_path= op.ref_provider.ref_fasta_file.path
gtf_file= op.ref_provider.ref_gtf_file.path


####################
p= Project("mock", input_root_dir, replication_level = "lane")



t0= time.time()

r0= p.samples[0].replicates[0]
r0.concat_split_pairs(merge_split_dir= merge_split_dir, split= 20)
pairs= [pair for pair in r0.fastq_pairs]
fastq_pair= pairs[0]

t1= time.time()

print (t1-t0)


####################

trash="""
#### alignment
aln_provider= op.get_alignment_provider(fastq_pair.name)

aln_output_dir= aln_provider.__dict__[fastq_pair.name].path
sj_out=  aln_provider.sj_file.path
sam_out=  aln_provider.sam_file.path
count_out= aln_provider.count_file.path


aln= Aligner(
    fastq_pair= fastq_pair, 
    genome_dir1= genome_dir1, genome_dir2= genome_dir2, 
    genome_fasta_path= genome_fasta_path, sj_out= sj_out, 
    sam_out= sam_out, gtf_file= gtf_file, 
    count_out= count_out, 
    tmp_output_dir_1= tmp_output_dir_1, 
    tmp_output_dir_2= tmp_output_dir_2,
    output_dir= aln_output_dir)

aln.align_fastq_pair()
"""

trash_0="""
#### disk space for large temporary files
tmp_dir= os.environ["SNIC_TMP"]
output_base= tmp_dir
genome_dir1= "/proj/b2016253/nobackup/genomeDir"
genome_dir2= os.path.join(tmp_dir, "genomeDir_%s" %(s_no))

if not os.path.exists(genome_dir2):
    os.mkdir(genome_dir2)

genome_dir3= genome_dir2
genome_fasta_path= "/proj/b2016253/nobackup/GRCh38.d1.vd1.fa"

output_dir= "/home/adilm/repos/utopyia/utopyia/rnaseq/output/%s" % s_no

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


tmp_output_dir_1= os.path.join(tmp_dir, "tmp_1/")
tmp_output_dir_2= os.path.join(tmp_dir, "tmp_2/")
#tmp_output_dir_2= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/tmp_2/"

if os.path.exists(tmp_output_dir_1):
    shutil.rmtree(tmp_output_dir_1)

if os.path.exists(tmp_output_dir_2):
    shutil.rmtree(tmp_output_dir_2)



sj_out= os.path.join(output_dir, "SJ.out.tab")
sam_output= os.path.join(output_dir, "Aligned.sortedByCoord.out.bam")
gtf_file= "/proj/b2016253/nobackup/gencode.v22.annotation.gtf"
count_output= os.path.join(output_dir, "count.txt")

"""


trash="""
test_data_base= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_data/"

fastq_1= os.path.join(test_data_base, "reads_1.fastq.gz")
fastq_2= os.path.join(test_data_base, "reads_2.fastq.gz")

fastq_pair= (fastq_1, fastq_2)

aln= Aligner(fastq_pair=fastq_pair, genome_dir1=genome_dir1, genome_dir2=genome_dir2, 
        genome_fasta_path=genome_fasta_path, sj_out=sj_out, 
        sam_out= sam_output, gtf_file=gtf_file, count_out= count_output, 
        tmp_output_dir_1= tmp_output_dir_1, tmp_output_dir_2= tmp_output_dir_2,
        output_dir= output_dir)

aln.align_fastq_pair()
"""



