import os
import shutil
from collections import OrderedDict
from operator import itemgetter
from itertools import izip

from concator import FastQConcator
from splitter import FastQSplitter
from file_learner import FastQFileLearner

import pdb




class FastQController(object):
    
    def __init__(self, container, fname_column_separator="_", fname_read_index=-1, fname_order_index=0, fname_extension=".fastq.gz", max_n_seq= 5000, merge_split_dir="", sample_name= ""):
        
        self.max_n_seq= max_n_seq
        self.container= container
            
        self.merge_split_dir= merge_split_dir

        self.sample_name= sample_name

        self.learner= FastQFileLearner(fname_column_separator, fname_read_index, fname_order_index, fname_extension)
        self.pairs= OrderedDict()   


    def extract_pairs(self):
        files= self.container.fastq_files
        pairs= {}
        for fastq_file in files:
            self.learner.set_file(fastq_file)
            
            if self.learner.order_id not in pairs:
                pairs[self.learner.order_id]= [None, None]

            pairs[self.learner.order_id][self.learner.pair_id-1] = fastq_file
        
        self.pairs= OrderedDict(sorted(pairs.items()))
        return self.pairs


    def concat(self):
        
        ordered_fastq_pairs= self.extract_pairs()

        reads_1 = map(itemgetter(0), ordered_fastq_pairs.values())
        reads_2 = map(itemgetter(1), ordered_fastq_pairs.values())

        f_cols_1= os.path.basename(reads_1[0]).split(self.learner.fname_column_separator)
        f_cols_1.pop(self.learner.fname_order_index)
            
        f_cols_2= os.path.basename(reads_2[0]).split(self.learner.fname_column_separator)
        f_cols_2.pop(self.learner.fname_order_index)
            
      
        merged_name_1 =   self.learner.fname_column_separator.join(f_cols_1)
        merged_name_2 =   self.learner.fname_column_separator.join(f_cols_2)
        
             
        merged_full_path1 = FastQConcator(compressed_file_paths= reads_1, 
                root_dir= self.merge_split_dir, sample_name= self.sample_name, 
                merged_file_name= merged_name_1).merged_file_path
        
        merged_full_path2 = FastQConcator(compressed_file_paths= reads_2, 
                root_dir= self.merge_split_dir, sample_name= self.sample_name, 
                merged_file_name= merged_name_2).merged_file_path
                
        

        self.pairs = OrderedDict({1:(merged_full_path1, merged_full_path2)})
        
        return self.pairs


    def yield_split_pairs(self):        
        fastq_1_handle= FastQSplitter(file_path= self.pairs.values()[0][0], 
                root_dir= self.merge_split_dir, sample_name= self.sample_name, 
                n_seq= self.max_n_seq).run()
        
        fastq_2_handle= FastQSplitter(file_path= self.pairs.values()[0][1], 
                root_dir= self.merge_split_dir, sample_name= self.sample_name, 
                n_seq= self.max_n_seq).run()

        return fastq_1_handle, fastq_2_handle



