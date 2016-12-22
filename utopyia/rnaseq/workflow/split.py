import sys
sys.path.append("../")


from task import Task, TaskIOProvider
from fastq.splitter import FastQSplitter, FastQContainerSplitter

from config.task_params import max_n_seq, compression_method
from config.task_io import gen_split_io

class SplitIOProvider(TaskIOProvider):
    def __init__(self, root_dir, tmp_dirs, **kwargs):
        TaskIOProvider.__init__(self, root_dir= root_dir, tmp_dirs= tmp_dirs)



class SplitContainer(Task):
    def __init__(self, fastq_container, log_message=""):
        
        split_io= gen_split_io(fastq_container)
        split_io_provider = SplitIOProvider(**split_io )
        
        Task.__init__(self, split_io_provider, log_message)
        self.fastq_container= fastq_container

    def run(self, **kwargs):
        """
            returns a generator of fastq_pairs
        """

        self.init_params(**kwargs)
        
        tmp_params= self.io_provider.tmp_provider
        
        split_dir= tmp_params.split_dir.path
        

        splitter= FastQContainerSplitter(self.fastq_container, split_dir, 
                     n_seq= self.n_seq,
                     compression_method= self.compression_method)
        
        for result in splitter.split_container():
            for pair in result:
                yield pair


    def init_params(self):
        self.compressed= True
        self.n_seq= max_n_seq
        self.compression_method= compression_method


trash= """
class Split(Task):
    def __init__(self, log_message=""):
        io_provider = SplitIOProvider(root_dir= split_dir, tmp_dirs=  )
        Task.__init__(self, io_provider, log_message)

    def run(self, **kwargs):
        
        self.init_params(**kwargs)
        
        input_params= self.io_provider.input_provider
        output_params= self.io_provider.output_provider
        
        file_path= input_params.file_path
        split_dir= output_params.split_dir
        

        splitter= FastQSplitter(file_path= file_path, split_dir= split_dir
                     compressed= self.compressed, n_seq= self.n_seq,
                     compression_method= self.compression_method)
        
        splitter.split(decompress= True)


    def init_params(self, **kwargs):
        self.compressed= True
        self.n_seq= max_n_seq
        self.compression_method= compression_method

        if "compressed" in kwargs:
            self.compressed= kwargs["compressed"]
            
        if "compression_method" in kwargs:    
            self.compression_method= kwargs["compression_method"]

        if "n_seq" in kwargs:
            self.n_seq= kwargs["n_seq"]

"""


