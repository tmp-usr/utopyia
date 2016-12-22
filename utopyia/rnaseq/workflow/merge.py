import sys
sys.path.append("../")



from task import Task, TaskIOProvider
from fastq.merger import FastQMerger

from config.task_io import gen_merge_io

class MergeIOProvider(TaskIOProvider):
    def __init__(self, root_dir, input_files, output_dirs, output_files, **kwargs):
        TaskIOProvider.__init__(self, root_dir= root_dir, 
                                input_files= input_files,
                                output_dirs= output_dirs,
                                output_files= output_files)
                                                    

class MergeContainer(Task):
    def __init__(self, fastq_container, log_message=""):
        merge_io= gen_merge_io(fastq_container)
        merge_io_provider= MergeIOProvider(**merge_io)
        
        Task.__init__(self, split_io_provider, log_message)
        self.fastq_container= fastq_container


    def run(self):
        tmp_params= self.io_provider.tmp_provider
        merged_dir= tmp_params.merge_dir

        merger= FastQContainerMerger(self.fastq_container, merge_dir)
        return merger.merge()



class Merge(Task):
    def __init__(self, merge_io_provider, log_message=""):
        Task.__init__(self, split_io_provider, log_message)

    def run(self):
        input_params= self.io_provider.input_provider
        output_params= self.io_provider.output_provider
        
        file_paths= input_params.file_paths
        merged_file_path= output_params.merged_file_path

        merger= FastQMerger(file_paths, merged_file_path)
        merger.merge()

