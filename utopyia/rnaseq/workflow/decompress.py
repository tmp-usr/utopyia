from task import Task, TaskIOProvider
from fastq.splitter import FastQSplitter


class SplitIOProvider(TaskIOProvier):
    def __init__(self, root_dir, input_files, output_dirs, output_files}
        TaskIOProvider.__init__(self, root_dir= root_dir, 
                                input_files= input_files,
                                output_dirs= output_dirs,
                                output_files= output_files)
                                                    

class Split(Task):
    def __init__(self, split_io_provider, log_message=""):
        Task.__init__(self, split_io_provider, log_message)

    def run(self):
        FastQSplitter()


