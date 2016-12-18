import os
import sys

sys.path.append(os.path.join(os.path.abspath("."),'..'))

import shutil
from collections import OrderedDict
from operator import itemgetter
from itertools import izip

from concator import FastQConcator
from splitter import FastQSplitter
from file_learner import FastQFileLearner

import pdb


class FastQContainer(object):
    """
        @fname_column_splitter: splitter that extract fields from a filename
        @read_column_no: the column number that the read_pair info is kept
        @file_order_column_no: the column number where the lane/replicate/sample
        number information is kept in situations where we would like to concatenate
        fastq files at a given level.
    """

    def __init__(self, name, dirpath, fastq_files=[], fname_column_separator="_", fname_read_index=-1, fname_order_index=0, fname_extension="fastq.gz"):
        ##
        self.name = name
        self.dirpath= dirpath
        self.fastq_files = fastq_files
        ##
        self.merged_pair= [None, None]
        ##
        self.concat= False
        self.split= False
        
        self.learner= FastQFileLearner(fname_column_separator, fname_read_index, fname_order_index, fname_extension)
    


trash2= """

    def extract_pairs(self):
        
        files= self.fastq_files
        pairs= {}
        for fastq_file in files:
            self.learner.set_file(fastq_file)
            
            if self.learner.order_id not in pairs:
                pairs[self.learner.order_id]= [None, None]
            pairs[self.learner.order_id][self.learner.pair_id-1] = fastq_file
        return OrderedDict(sorted(pairs.items()))



    def concat_split_pairs(self, merge_split_dir=".", concat= True,  n_seq= None, sample_name=""):
        '''
            - concatenates the divided sample data into one and splits into a user defined
            number of smaller compressed files.
            - returns either the merged pair or the pairs of read iles.
        '''
        
        if concat:

            file_order_fastq_pairs= self.extract_pairs()

            reads_1 = map(itemgetter(0), file_order_fastq_pairs.values())
            reads_2 = map(itemgetter(1), file_order_fastq_pairs.values())

            f_cols_1= os.path.basename(reads_1[0]).split(self.fname_column_separator)
            f_cols_1.pop(self.forder_index)
            
            f_cols_2= os.path.basename(reads_2[0]).split(self.fname_column_separator)
            f_cols_2.pop(self.forder_index)
            
            
            merged_name_1 =   self.fname_column_separator.join(f_cols_1)
            merged_name_2 =   self.fname_column_separator.join(f_cols_2)


            if merge_split_dir == ".":
                merge_split_dir = os.path.dirname(reads_1[0])

            fastq_id= "%s_%s" %(sample_name, self.name)
            
            
            
            
            cc1 = ConcatenateCompressed(compressed_file_paths= reads_1, root_dir= merge_split_dir, 
                    sample_name= fastq_id, merged_file_name= merged_name_1).merged_file_path
            cc2 = ConcatenateCompressed(compressed_file_paths= reads_2, root_dir= merge_split_dir, 
                    sample_name= fastq_id, merged_file_name= merged_name_2).merged_file_path
                
            
            
            self.merged_pair[0] = cc1 
            self.merged_pair[1] = cc2 
            
            self.concat= True

            if n_seq:
                fastq_1_handle= FastQSplitter(file_path= self.merged_pair[0], 
                        root_dir= merge_split_dir, sample_name= fastq_id, n_seq= n_seq).run()
                fastq_2_handle= FastQSplitter(file_path= self.merged_pair[1], 
                        root_dir= merge_split_dir, sample_name= fastq_id, n_seq= n_seq).run()

                return fastq_1_handle, fastq_2_handle

                #pdb.set_trace()
                
                #self.split= True
                #return zip(self.splitter_1.split_fastq_files, self.splitter_2.split_fastq_files )

            #else:
            #    return cc1, cc2
"""

trash= """
    @property
    def fastq_pairs(self):
        if self.concat:
            if self.split:
                for reads_1, reads_2 in zip(self.splitter_1.split_fastq_files, self.splitter_2.split_fastq_files ):
                    ### check how this change is gonna effect
                    self.name = os.path.basename(reads_1.replace(".fastq.gz",""))
                    yield FastQPair(reads_1, reads_2, self.name)
            else:
                yield FastQPair(self.merged_pair[0], self.merged_pair[1], self.name)

        else:
            for reads_1, reads_2 in self.extract_pairs().values():
                yield FastQPair(reads_1, reads_2, self.name)
"""
