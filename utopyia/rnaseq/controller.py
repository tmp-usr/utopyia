import os
import shutil
from itertools import izip


from aligner import Aligner
from project.project import Project
from config.file_provider import RNASeqIOProvider
from project.fastq_container import FastQPair


from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


import time

import pdb


class Controller(object):
    def __init__(self, project_name, replication_level="lane"):

        self.io_provider= RNASeqIOProvider()

        self.input_root_dir= self.io_provider.input_root_dir

        #### tmp
        self.tmp_output_dir_1=  self.io_provider.tmp_provider.tmp_output_dir_1.path
        self.tmp_output_dir_2=   self.io_provider.tmp_provider.tmp_output_dir_2.path
        self.merge_split_dir= self.io_provider.tmp_provider.merge_split_dir.path

        #### reference
        self.genome_dir1= self.io_provider.ref_provider.ref_genome_dir.path
        self.genome_dir2= self.io_provider.tmp_provider.reindexed_genome_dir.path
        self.genome_fasta_path= self.io_provider.ref_provider.ref_fasta_file.path
        #self.gtf_file= self.io_provider.ref_provider.ref_gtf_file.path
        self.gtf_file= ""

        ####################
        self.project= Project(project_name, self.input_root_dir, replication_level = replication_level)

        self.init_samples()
        #self.run_parallel()

    def init_samples(self):
        self.all_replicates={}
        for sample in self.project.samples:
            for replicate in sample.replicates:
                self.all_replicates[replicate] = sample
                

    def init_alignment(self, replicate):
        """
            Method where the actual pipeline takes place.
        """
        #for replicate in sample.replicates:
        #    #self.all_replicates[replicate] = sample
        
        #sample= self.all_replicates[replicate]
        self.io_provider.refresh_tmp()
        pair1, pair2= replicate.concat_split_pairs(merge_split_dir= self.merge_split_dir, n_seq= 5000, sample_name= replicate.name)
        

        sample = self.all_replicates[replicate]
        
        for (i, reads_1), (i, reads_2) in izip(pair1, pair2):
            
            fastq_pair= FastQPair(reads_1, reads_2, name= replicate.name)

            aln_name= "%s_%s_%d" %(sample.name, replicate.name, i) 
            self.aln_provider= self.io_provider.get_alignment_provider(aln_name)

            self.aln_output_prefix= self.aln_provider.prefix.path
            
            self.sj_out=  self.aln_provider.sj_file.path
            self.sam_out=  self.aln_provider.bam_file.path
            self.count_out= self.aln_provider.count_file.path


            aln= Aligner(
                fastq_pair= fastq_pair,
                genome_dir1= self.genome_dir1, genome_dir2= self.genome_dir2, 
                genome_fasta_path= self.genome_fasta_path, sj_out= self.sj_out, 
                sam_out= self.sam_out, gtf_file= self.gtf_file, 
                count_out= self.count_out, 
                tmp_output_dir_1= self.tmp_output_dir_1, 
                tmp_output_dir_2= self.tmp_output_dir_2,
                output_prefix= self.aln_output_prefix)

            aln.align_fastq_pair()

    def run_parallel(self):
        p= Pool(processes= 2)
        p.map(self.init_alignmen, dict(self.all_replicates.items()[:2]))#self.all_replicates)
        

if __name__ == "__main__":
    c= Controller("mock")
    c.init_alignment(dict(c.all_replicates.items()).keys()[0])
    #[c.init_alignment(rep) for rep in c.all_replicates]
    #c.run_parallel() 
    




