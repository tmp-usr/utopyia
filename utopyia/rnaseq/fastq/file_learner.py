import os

import pdb

class FastQFileLearner(object):
    def __init__(self, fname_column_separator, fname_read_index, fname_order_index, fname_extension=""):
        
        self.fname_column_separator= fname_column_separator
        self.fname_read_index= fname_read_index
        self.fname_order_index= fname_order_index
        self.fname_extension= ".fastq%s" %fname_extension
        self.file_path = None

    def set_file(self, file_path):
        self.file_path = file_path
    
    def trim_extension(self, ext= ""):
        trimmed= self.fname
        while os.path.splitext(trimmed)[1] != '':trimmed= os.path.splitext(trimmed)[0]
        return trimmed

    @property
    def fname(self):
        return os.path.basename(self.file_path)

    @property
    def fname_fields(self):
        return os.path.basename(self.file_path).replace(
                self.fname_extension, "").split(
                self.fname_column_separator)

    @property
    def pair_id(self):
        return int(self.fname_fields[self.fname_read_index])

    @property
    def order_id(self):
        return self.fname_fields[self.fname_order_index]


 

