import os
import shutil
from rnaseq_config import *


class Reference(object):
    def __init__(self, species_name= "homo sapiens", genome_dir= "", fasta_file= "", gtf_file= ""):
        self.species_name= species_name
        self.genome_dir= genome_dir
        self.fasta_file= fasta_file
        self.gtf_file= gtf_file


class TemporaryOutput(object):
    def __init__(self, root_dir, directories=[], file_types= []):
        self.root_dir= root_dir
        self.directories= directories
        self.file_types= file_types


    @property
    def dirs(self):
        return {tmp_type: self.get_dir(tmp_type) for tmp_type in self.directories}
                
    @property
    def files(self):
        return {tmp_type: self.get_files(tmp_type) for tmp_type in self.files}
                


    def get_dir(self, tmp_type, create= True):
        tmp_dir= os.path.join(self.root_dir, tmp_type)
        
        if create:
            if os.path.exists(tmp_dir):
               shutil.rmtree(tmp_dir) 
            
            if "tmp_output" not in tmp_type:
                os.makedirs(tmp_dir)



        return tmp_dir

    def get_file(self, tmp_type):
        return os.path.join(root_dir, tmp_type)



class FileProviderBase(object):
    
    def __init__(self, ref_genome_dir, ref_fasta_file, ref_gtf_file, tmp_root_dir, output_dir):
        self.reference= Reference(ref_genome_dir, ref_fasta_file, ref_gtf_file)
        tmp_dirs= ["merge_split", "decompression", "alignment", "reindexed_genome",
                   "tmp_output_dir_1", "tmp_output_dir_2"]
        self.tmp_dirs= TemporaryOutput(tmp_root_dir, tmp_dirs).dirs
        self.output_dir= output_dir



class FileProvider(FileProviderBase):
    def __init__(self):
        output_types= {"sam": ".sam", "sj":"sj.txt", "count": "count.txt"}
        FileProviderBase.__init__(self, ref_genome_dir, ref_fasta_file, ref_gtf_file, tmp_root_dir, output_base_dir)
        self.output_types= output_types
        self.outputs= None

    def set_outputs(self, fastq_pair):
        self.outputs= {output_type: os.path.join(self.output_dir, "%s_%s" %(fastq_pair.name, file_name)) for output_type, file_name in self.output_types.iteritems()}

    def get_output_file(self, fastq_pair, output_type):
        if not self.outputs:
            self.set_outputs(fastq_pair)

        else:
            return self.outputs[output_type]
