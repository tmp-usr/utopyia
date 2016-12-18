import os
import shutil
from itertools import izip


from alignment.aligner import Aligner
from project.project import Project
from helper.file_provider import RNASeqIOProvider
from fastq.pair import FastQPair
from fastq.controller import FastQController

from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


import time

import pdb


class Utopyia(object):
    def __init__(self, project_name, replication_level="lane"):

        self.io_provider= RNASeqIOProvider()

        self.input_root_dir= self.io_provider.input_root_dir

        #### tmp
        self.merge_split_dir= self.io_provider.tmp_provider.merge_split_dir.path

        #### reference
        self.genome_dir1= self.io_provider.ref_provider.ref_genome_dir.path
        self.genome_fasta_path= self.io_provider.ref_provider.ref_fasta_file.path
        self.gtf_file= self.io_provider.ref_provider.ref_gtf_file.path

        ####################
        self.project= Project(project_name, self.input_root_dir, 
                replication_level = replication_level)

        self.init_samples()
        #self.run_parallel()



    def init_samples(self):
        self.all_replicates={}
        for sample in self.project.samples:
            for replicate in sample.replicates:
                self.all_replicates[replicate] = sample
                
 
    def concat_split_pairs(self, replicate,
            merge_split_dir= "", 
            n_seq= None):
        
        sample_name = self.all_replicates[replicate].name

        fq_controller= FastQController(replicate, merge_split_dir= self.merge_split_dir, sample_name= sample_name)

        fq_controller.concat()
        pair1, pair2 = fq_controller.yield_split_pairs()
      
        return pair1, pair2


    def init_alignment(self, replicate):

        j= 0
        pair1, pair2= self.concat_split_pairs(replicate)
        sample_name = self.all_replicates[replicate].name

        for (i, reads_1), (i, reads_2) in izip(pair1, pair2):
            j+=1 
            
            fastq_pair= FastQPair(reads_1, reads_2, name= replicate.name)

            aln_name= "%s_%s_%d" %(sample_name, replicate.name, i) 
            self.aln_provider= self.io_provider.get_alignment_provider(aln_name)

            self.aln_output_prefix= self.aln_provider.prefix.path
            
            self.sj_out=  self.aln_provider.sj_file.path
            self.sam_out=  self.aln_provider.bam_file.path
            self.count_out= self.aln_provider.count_file.path
            
            self.aln_tmp_provider= self.io_provider.get_alignment_tmp_provider(aln_name)
            
            self.genome_dir2= self.aln_tmp_provider.reindexed_genome_dir.path
            self.tmp_output_dir1= self.aln_tmp_provider.tmp_output_dir1.path
            self.tmp_output_dir2= self.aln_tmp_provider.tmp_output_dir2.path
                 

            if j == 1:
                pdb.set_trace()
                break


        
    def run_parallel(self):
        p= Pool(processes= 2)
        p.map(self.init_alignmen, dict(self.all_replicates.items()[:2]))#self.all_replicates)
        

if __name__ == "__main__":
    c= Controller("mock")
    rep= dict(c.all_replicates.items()).keys()[0]

    #[c.init_alignment(rep) for rep in c.all_replicates]
    #c.run_parallel() 
    



trash="""
    def init_alignment(self, replicate):
        '''
            Method where the actual pipeline takes place.
        '''
        #for replicate in sample.replicates:
        #    #self.all_replicates[replicate] = sample
        
        #sample= self.all_replicates[replicate]
        self.io_provider.refresh_tmp()
        
        pair1, pair2= replicate.concat_split_pairs(
                merge_split_dir= self.merge_split_dir, n_seq= 5000, 
                sample_name= replicate.name )
        

        sample = self.all_replicates[replicate]
        
        for (i, reads_1), (i, reads_2) in izip(pair1, pair2):
            
            fastq_pair= FastQPair(reads_1, reads_2, name= replicate.name)

            aln_name= "%s_%s_%d" %(sample.name, replicate.name, i) 
            self.aln_provider= self.io_provider.get_alignment_provider(aln_name)

            self.aln_output_prefix= self.aln_provider.prefix.path
            
            self.sj_out=  self.aln_provider.sj_file.path
            self.sam_out=  self.aln_provider.bam_file.path
            self.count_out= self.aln_provider.count_file.path
            
            self.aln_tmp_provider= self.io_provider.get_alignment_tmp_provider(aln_name)
            
            self.genome_dir2= self.aln_tmp_provider.reindexed_genome_dir.path
            self.tmp_output_dir1= self.aln_tmp_provider.tmp_output_dir1.path
            self.tmp_output_dir2= self.aln_tmp_provider.tmp_output_dir2.path

            
            
            aln= Aligner(
                fastq_pair= fastq_pair,
                genome_dir1= self.genome_dir1, genome_dir2= self.genome_dir2, 
                genome_fasta_path= self.genome_fasta_path, sj_out= self.sj_out, 
                sam_out= self.sam_out, gtf_file= self.gtf_file, 
                count_out= self.count_out, 
                tmp_output_dir_1= self.tmp_output_dir1, 
                tmp_output_dir_2= self.tmp_output_dir2,
                output_prefix= self.aln_output_prefix)

            aln.align_fastq_pair()
"""


trash="""          
            aln= Aligner(
                fastq_pair= fastq_pair,
                genome_dir1= self.genome_dir1, genome_dir2= self.genome_dir2, 
                genome_fasta_path= self.genome_fasta_path, sj_out= self.sj_out, 
                sam_out= self.sam_out, gtf_file= self.gtf_file, 
                count_out= self.count_out, 
                tmp_output_dir_1= self.tmp_output_dir1, 
                tmp_output_dir_2= self.tmp_output_dir2,
                output_prefix= self.aln_output_prefix)

            aln.align_fastq_pair()
"""
   
