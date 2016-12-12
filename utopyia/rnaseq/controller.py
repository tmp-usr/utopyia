import os
import shutil

from aligner import Aligner
from project.project import Project
from config.file_provider import RNASeqIOProvider

from multiprocessing import Pool

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


all_replicates=[]


for sample in p.samples:
    for replicate in sample.replicates:
        for fastq_file in replicate.fastq_files:
            print sample.name, replicate.name, fastq_file
        
        #all_replicates.append(replicate)
        

def merge_split_align_replicate(replicate):
    r0= replicate
    r0.concat_split_pairs(merge_split_dir= merge_split_dir, split= 1)
    pairs= [pair for pair in r0.fastq_pairs]
    fastq_pair= pairs[0]

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

#with Pool() as p:
#    p.map(merge_split_align_replicate, all_replicates[:2])


