from janitor.io_provider import InputProvider, OutputProvider, TmpProvider


class TaskIOProvider(object):
    def __init__(self, root_dir, input_dirs={}, input_files={}, 
                                 output_dirs={}, output_files={},
                                 tmp_dirs= {}, tmp_files= {}):
        self.root_dir= root_dir
        self.input_provider= InputProvider(root_dir, input_dirs, input_files)
        self.output_provider= OutputProvider(root_dir, output_dirs, output_files)
        self.tmp_provider= TmpProvider(root_dir, tmp_dirs, tmp_files)
 

class Task(object):
    def __init__(self, io_provider, log_message=""):
        self.io_provider = io_provider
        self.log_message = log_message

    def run(self):
        pass


class Dependence(object):
    def __init__(self, task1, task2):
        self.task1= task1
        self.task2= task2
        
    def get_pass(self):
        """
            Checks if the input files for the task2 
            actually exists among the outputs of task1.
        """
        pass



