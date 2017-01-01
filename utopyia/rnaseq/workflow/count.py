import sys
import os
sys.path.append("../")

from task import Task, TaskIOProvider
from alignment.aligner import Aligner

from config.task_io import gen_count_io
from alignment.counter import Counter

import pdb


class CountIOProvider(TaskIOProvider):
    def __init__(self, root_dir, output_files, **kwargs):
        TaskIOProvider.__init__(self, root_dir= root_dir, 
                                output_files= output_files,
                                **kwargs)
                                                    

class Count(Task):
    def __init__(self, level= "gene", method= "kallisto", log_message="", **kwargs):
        
        self.method= method
        self.level = level
       
        count_io = gen_count_io()
        count_io_provider = CountIOProvider(**count_io)
        
        Task.__init__(self, count_io_provider, log_message)
        
        
        self.sample_output_paths = {}

    def set_alignment_outputs(self):
        path = self.io_provider.root_dir
        path = os.path.normpath(path)

        ###  copied the below loop from
        ###  http://stackoverflow.com/a/7159726
        for root,dirs,files in os.walk(path, topdown=True):
            depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
            if depth == 1:
                sample_dir_names= root.split(os.path.sep)
                sample_name= sample_dir_names[-2]
                if sample_name not in self.sample_output_paths:
                    self.sample_output_paths[sample_name] = {}
                
                tmp_dict= {sample_dir_names[-1]: os.path.join(root, "abundance.tsv")}
                self.sample_output_paths[sample_name].update(tmp_dict)
                dirs= []
        return self.sample_output_paths

    def count(self, sample_output_paths):
        
        if self.level == "gene":
            output_abundance_path= self.io_provider.output_provider.gene.path
        else:
            output_abundance_path= self.io_provider.output_provider.transcript.path
        
        cnt= Counter(sample_output_paths, output_abundance_path, level= self.level)
        return cnt.generate_counts()


# dependence class can be generalized by using the io providers of indidual steps
# e.g. output_files of an io_provider of a task class can be arranged to be the
# input files of the next task.

