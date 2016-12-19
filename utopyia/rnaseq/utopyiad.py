import os
import shutil
from itertools import izip


from alignment.aligner import Aligner
from project.project import Project
from helper.file_provider import RNASeqIOProvider
from fastq.pair import FastQPair
from fastq.controller import FastQController
from config.rnaseq_config import compression_method


from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


import time

import pdb


class Utopyia(object):
    def __init__(self, project_name, replication_level= "replicate"):

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
        self.all_fastq_containers={}
        for sample in self.project.samples:
            
            if self.project.replication_level == "replicate":
                self.all_fastq_containers[sample]  = sample

            elif self.project.replication_level == "lane": 
                for replicate in sample.replicates:
                    self.all_fastq_containers[replicate] = sample
                
 
    def concat_split_pairs(self, fastq_container,
            merge_split_dir= "", 
            concat= False,
            max_n_seq= 5000):
        
        pdb.set_trace()

        self.sample_name = self.all_fastq_containers[fastq_container].name
        
        if merge_split_dir == "":
            merge_split_dir= self.merge_split_dir

        fq_controller= FastQController(fastq_container, merge_split_dir= merge_split_dir, sample_name= self.sample_name, max_n_seq= max_n_seq, compression_method= compression_method)
        

        if concat == True:
            ### _pairs is a dict whereas result_pairs is a generator
            _pairs= fq_controller.concat()
       
        if max_n_seq != None:
            return fq_controller.yield_split_pairs()
        
        

    def init_alignment(self, fastq_container, fastq_pair_generator):
        j=0
        for result in fastq_pair_generator:
            for i, pair in enumerate(result, 1):
                
                j+=1
                
                print pair

                ### general inputs
                fastq_pair= FastQPair(pair[0], pair[1], name= fastq_container.name)
                
                aln_name= "%s_%s_%d" %(self.sample_name, fastq_container.name, i) 
                aln_provider= self.io_provider.get_alignment_provider(aln_name)
                
            

                ### star inputs
                aln_output_prefix= aln_provider.prefix.path
                
                self.sj_out=  aln_provider.sj_file.path
                self.sam_out=  aln_provider.bam_file.path
                self.count_out= aln_provider.count_file.path
                
                aln_tmp_provider= self.io_provider.get_alignment_tmp_provider(aln_name)
                
                self.genome_dir2= aln_tmp_provider.reindexed_genome_dir.path
                self.tmp_output_dir1= aln_tmp_provider.tmp_output_dir1.path
                self.tmp_output_dir2= aln_tmp_provider.tmp_output_dir2.path
            
                
                # kallisto_inputs
                self.genome_index= self.io_provider.ref_provider.genome_index
                self.output_dir= aln_provider.__dict__[aln_name]


                aln= Aligner(
                    fastq_pair= fastq_pair,
                    output_dir= self.output_dir,
                    genome_index= self.genome_index)

                aln.align_fastq_pair()


                if j == 1:
                    pdb.set_trace()
                    break

                



        
    def run_parallel(self):
        p= Pool(processes= 2)
        p.map(self.init_alignmen, dict(self.all_fastq_containers.items()[:2]))#self.all_replicates)
        

if __name__ == "__main__":
    #c= Utopyia("mock", replication_level="replicate")
    c= Utopyia("mock", replication_level="replicate")
    rep= dict(c.all_fastq_containers.items()).keys()[0]
    fastq_pair_generator= c.concat_split_pairs(rep, concat= False, max_n_seq= 10000)
    c.init_alignment(rep, fastq_pair_generator)
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
            
            self.output_dir= 
            
            
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

