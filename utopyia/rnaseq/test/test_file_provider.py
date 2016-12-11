import sys
import os

sys.path.append(os.path.join(os.path.abspath("."),'..'))

from config.file_provider import RNASeqIOProvider
from project.project import Project

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


#t0= time.time()

r0= p.samples[0].replicates[0]
r0.concat_split_pairs(merge_split_dir= merge_split_dir, split= 1)
pairs= [pair for pair in r0.fastq_pairs]
fastq_pair= pairs[0]
####################


#### alignment
aln_provider= op.get_alignment_provider(fastq_pair.name)

aln_output_dir= aln_provider.__dict__[fastq_pair.name].path
sj_out=  aln_provider.sj_file.path
sam_out=  aln_provider.sam_file.path
count_out= aln_provider.count_file.path


#t1= time.time()


print "#######"
print "Raw data"
print "Raw data dir: ", input_root_dir
print "#######"
print "Reference Genome Related paths"
print "Reference genome dir: ", genome_dir1
print "Reindexed genome dir: ", genome_dir2
print "Genome fasta file: ", genome_fasta_path
print "Genome GTF File path", gtf_file
print "#######"
print "Alignment related paths"
print "All alignment outputs:", aln_output_dir
print "SJ file: ", sj_out
print "SAM file: ", sam_out
print "Count output file: ", count_out
print "#######"
print "Temporary Outputs"
print "Merge/split dir: ", merge_split_dir
print "Temporary alignment outputs: ", tmp_output_dir_1, tmp_output_dir_2












 

