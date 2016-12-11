import os
import shutil

from janitor.output_provider import OutputProvider

from rnaseq_config import *

import pdb


class ReferenceProvider(OutputProvider): 
    def __init__(self, root_dir, genome_dir= "genome_dir", fasta_file= "",
                      gtf_file= "", species_name= "homo sapiens"):

        dirs= {"genome_dir": os.path.join(root_dir, genome_dir)}
        files= {"fasta_file": os.path.join(root_dir, fasta_file), 
                "gtf_file": os.path.join(root_dir, gtf_file)}

        OutputProvider.__init__(self, root_dir, dirs, files)
        self.species_name= species_name


class TmpProvider(OutputProvider):
    def __init__(self, root_dir):
        
        if create:
            if os.path.exists(tmp_dir):
               shutil.rmtree(tmp_dir) 
            
            if "tmp_output" not in tmp_type:
                os.makedirs(tmp_dir)

        tmp_dirs= ["merge_split_dir", "decompression_dir", "reindexed_genome_dir",
                   "tmp_output_dir_1", "tmp_output_dir_2"]

        tmp_dirs= {dir_name: os.path.join(root_dir, dir_name) for dir_name in tmp_dirs}
        OutputProvider.__init__(self, root_dir, tmp_dirs)


class AlignmentProvider(OutputProvider):
    def __init__(self, root_dir, sample_name):
        files= {"sam_file": os.path.join(root_dir, sample_name, "%s.sam" %sample_name ), 
                "sj_file": os.path.join(root_dir, sample_name, "%s.sj" %sample_name), 
                "count_file": os.path.join(root_dir, sample_name, "%s.count" %sample_name)}
        dirs= {
                sample_name: os.path.join(root_dir, sample_name)
                } 
        
        OutputProvider.__init__(self, root_dir, dirs= dirs, files= files)

        

class RNASeqOutputProvider(object):
    
    def __init__(self, output_root_dir= project_base_dir):

        self.output_root_dir= output_root_dir

        self.ref_provider= ReferenceProvider(root_dir= ref_root_dir, 
                genome_dir= ref_genome_dir,
                fasta_file= ref_fasta_file ,  
                gtf_file= ref_gtf_file)

        self.tmp_provider= TmpProvider(root_dir= tmp_root_dir)
        self.alignment_root_dir= os.path.join(self.output_root_dir, "alignment")


    def get_alignment_provider(self, sample_name):
        return AlignmentProvider(self.alignment_root_dir, sample_name)
    
