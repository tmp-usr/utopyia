import sys
sys.path.append("../")


from task import Task, TaskIOProvider
from fastq.splitter import FastQSplitter

from project.project import Project

from config.task_io import gen_project_io
from config.task_params import project_name, replication_level, fname_column_separator, \
                               fname_order_index, fname_read_index, fname_extension


class PopulateProjectIOProvider(TaskIOProvider):
    def __init__(self, root_dir, **kwargs):
        TaskIOProvider.__init__(self, root_dir= root_dir)



class PopulateProject(Task, Project):
    
    def __init__(self, log_message=""):

        project_io= gen_project_io()
        project_io_provider = PopulateProjectIOProvider(**project_io)
        
        Task.__init__(self, project_io_provider, log_message)

        self.init_params()
        
        root_dir= self.io_provider.root_dir
        
        Project.__init__(self, name= self.name, root_dir= root_dir,
                        replication_level= self.replication_level,
                        fname_column_separator= self.fname_column_separator, 
                        fname_read_index= self.fname_read_index, 
                        fname_order_index= self.fname_order_index, 
                        fname_extension= self.fname_extension)
        
    
        self.populate_fastq_containers()
        

    def init_params(self):
        self.name = project_name
        self.replication_level = replication_level
        self.fname_column_separator= fname_column_separator
        self.fname_read_index= fname_read_index
        self.fname_order_index= fname_order_index
        self.fname_extension= fname_extension
        
