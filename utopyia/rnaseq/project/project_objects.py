import sys
import os

sys.path.append(os.path.join(os.path.abspath("."),'..'))

from fastq.container import FastQContainer


class Sample(FastQContainer):
    
    def __init__(self, name, dirpath, fastq_files=[], fname_column_splitter="_", 
                read_column_no=-1, file_order_column_no=0):

        FastQContainer.__init__(self, name, dirpath, fastq_files, 
                            fname_column_splitter, read_column_no, 
                            file_order_column_no )

        self.replicates= []

    def add_replicate(self, replicate):
        self.replicates.append(replicate)


class Replicate(FastQContainer):
    
    def __init__(self, name, dirpath, fastq_files=[], fname_column_splitter="_", 
                read_column_no=-1, file_order_column_no=0):

        FastQContainer.__init__(self, name, dirpath, fastq_files, 
                            fname_column_splitter, read_column_no, 
                            file_order_column_no )

        self.lanes= []

    def add_lane(self, lane):
        self.lanes.append(lane)


class Lane(FastQContainer):
    
    def __init__(self, name, dirpath, fastq_files=[], fname_column_splitter="_", 
                read_column_no=-1, file_order_column_no=0):

        FastQContainer.__init__(self, name, dirpath, fastq_files, 
                            fname_column_splitter, read_column_no, 
                            file_order_column_no )






