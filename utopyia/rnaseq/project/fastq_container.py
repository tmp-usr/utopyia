import os
import shutil
from collections import OrderedDict
from operator import itemgetter


from concatenate_compressed import ConcatenateCompressed
from fastq_splitter import FastQSplitter


class FastQPair(object):
    def __init__(self, reads_1, reads_2, name= "", compressed= True, ):
        self.name = name
        self.reads_1 = reads_1
        self.reads_2 = reads_2
        self.compressed = compressed



class FastQContainer(object):
    """
        @fname_column_splitter: splitter that extract fields from a filename
        @read_column_no: the column number that the read_pair info is kept
        @file_order_column_no: the column number where the lane/replicate/sample
        number information is kept in situations where we would like to concatenate
        fastq files at a given level.

    """

    def __init__(self, name, dirpath, fastq_files=[], fname_column_separator="_", 
                read_index=-1, forder_index=0):

        self.name = name
        self.dirpath= dirpath
        self.fastq_files = fastq_files
        self.fname_column_separator= fname_column_separator
        self.read_index= read_index
        self.forder_index= forder_index
        self.merged_pair= [None, None]
        self.concat= False
        self.split= False
        

    def extract_pairs(self):
        files= self.fastq_files
        pairs= {}
        for fastq_file in files:
            metadata_fields = os.path.basename(fastq_file).split(self.fname_column_separator)
            file_order= int(metadata_fields[self.forder_index])
            pair_id= int(metadata_fields[self.read_index].replace(".fastq.gz",""))
            
            if file_order not in pairs:
                pairs[file_order]= [None, None]
            
            pairs[file_order][pair_id-1] = fastq_file
       
        return OrderedDict(sorted(pairs.items()))


    def concat_split_pairs(self, merge_split_dir=".", concat= True,  split=1):
        """
            - concatenates the divided sample data into one and splits into a user defined
            number of smaller compressed files.
            - returns either the merged pair or the pairs of read iles.
        """
        
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

            
            cc1 = ConcatenateCompressed(compressed_file_paths= reads_1, root_dir= merge_split_dir, 
                    sample_name= self.name, merged_file_name= merged_name_1).merged_file_path
            cc2 = ConcatenateCompressed(compressed_file_paths= reads_2, root_dir= merge_split_dir, 
                    sample_name= self.name, merged_file_name= merged_name_2).merged_file_path
                
            self.merged_pair[0] = cc1 
            self.merged_pair[1] = cc2 
            
            self.concat= True

            if split > 1:
                self.splitter_1= FastQSplitter(file_path= self.merged_pair[0], 
                        root_dir= merge_split_dir, sample_name= self.name, split_times= split )
                self.splitter_2= FastQSplitter(file_path= self.merged_pair[1], 
                        root_dir= merge_split_dir, sample_name= self.name, split_times= split)

                self.split= True
                return zip(self.splitter_1.split_fastq_files, self.splitter_2.split_fastq_files )

            else:
                return cc1, cc2


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

