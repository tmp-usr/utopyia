from collections import OrderedDict
import pdb


class FastQContainer(object):
    """
        @fname_column_splitter: splitter that extract fields from a filename
        @read_column_no: the column number that the read_pair info is kept
        @file_order_column_no: the column number where the lane/replicate/sample
        number information is kept in situations where we would like to concatenate
        fastq files at a given level.
    """

    def __init__(self, name, dirpath, fastq_files=[], learner= None):
        ##
        self.name = name
        self.dirpath= dirpath
        self.fastq_files = fastq_files
        ##
        self.learner= learner
    
    @property 
    def pairs(self):
        assert self.learner is not None, "File learner cannot be None!"
        assert self.fastq_files != [], "This might be an empty container, check again!"
        
        files= self.fastq_files
        pairs= {}
        for fastq_file in files:
            self.learner.set_file(fastq_file)
            
            if self.learner.order_id not in pairs:
                pairs[self.learner.order_id]= [None, None]

            pairs[self.learner.order_id][self.learner.pair_id-1] = fastq_file
        
        return OrderedDict(sorted(pairs.items()))

class Sample(FastQContainer):
    
    def __init__(self, name, dirpath, fastq_files=[], learner= None):
        FastQContainer.__init__(self, name, dirpath, fastq_files, learner)
        self.replicates= []

    def add_replicate(self, replicate):
        self.replicates.append(replicate)


class Replicate(FastQContainer):
    
    def __init__(self, name, dirpath, fastq_files=[], learner= None):
        FastQContainer.__init__(self, name, dirpath, fastq_files, learner) 
        self.lanes= []

    def add_lane(self, lane):
        self.lanes.append(lane)


class Lane(FastQContainer): 
    def __init__(self, name, dirpath, fastq_files=[], learner= None):
        FastQContainer.__init__(self, name, dirpath, fastq_files, learner)





