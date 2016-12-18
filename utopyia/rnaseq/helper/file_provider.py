import sys
import os
import shutil

sys.path.append(os.path.join(os.path.abspath("."),'..'))



from janitor.output_provider import OutputProvider

from config.rnaseq_config import *

import pdb


class ReferenceProvider(OutputProvider): 
    def __init__(self, root_dir, genome_dir= "genome_dir", fasta_file= "",
                      gtf_file= "", species_name= "homo sapiens"):

        dirs= {"ref_genome_dir": os.path.join(root_dir, genome_dir)}
        files= {"ref_fasta_file": os.path.join(root_dir, fasta_file),
                "ref_gtf_file": os.path.join(root_dir, gtf_file)}

        OutputProvider.__init__(self, root_dir, dirs, files)
        self.species_name= species_name


class TmpProvider(OutputProvider):
    def __init__(self, root_dir):
        tmp_dirs= ["merge_split_dir", "decompression_dir"]

        tmp_dirs= {dir_name: os.path.join(root_dir, dir_name) for dir_name in tmp_dirs}
        OutputProvider.__init__(self, root_dir, tmp_dirs)


    def get_reindexed_genome_dir(self, aln_name):
        return os.path.join(self.reindexed_genome_dir, aln_name) 



class AlignmentTmpProvider(OutputProvider):
    def __init__(self, tmp_dir, aln_name):
        self.root_dir = os.path.join(tmp_dir, aln_name)
        
        dirs= {
                "reindexed_genome_dir": os.path.join(self.root_dir, "reindexed_genome_dir"),
                "tmp_output_dir1": os.path.join(self.root_dir, "tmp_output_dir1"),
                "tmp_output_dir2": os.path.join(self.root_dir, "tmp_output_dir2")
                }

        OutputProvider.__init__(self, self.root_dir, dirs= dirs)



class AlignmentProvider(OutputProvider):
    """
        amend the file paths that replicate orders are also clarified.


    """
    
    def __init__(self, root_dir, aln_name):
        
        print "######### %s " %aln_name
        files= {"bam_file": os.path.join(root_dir, aln_name, "%sAligned.sortedByCoord.out.bam" %aln_name ), 
                "sj_file": os.path.join(root_dir, aln_name, "%sSJ.out.tab" %aln_name), 
                "count_file": os.path.join(root_dir, aln_name, "%s.count" %aln_name),
                "prefix": os.path.join(root_dir, aln_name, "%s" % aln_name)}

        dirs=   {
                 aln_name: os.path.join(root_dir, aln_name)
                } 
        OutputProvider.__init__(self, root_dir, dirs= dirs, files= files)





class RNASeqIOProvider(object):
    
    def __init__(self, project_root_dir= project_root_dir):

        self.project_root_dir= project_root_dir
        self.output_root_dir= os.path.join(self.project_root_dir, "outputs")
        self.input_root_dir= os.path.join(self.project_root_dir, "raw_data")

        #### refering to the symbolic links of the original reference files
        self.ref_provider= ReferenceProvider(root_dir= s_ref_root, 
                genome_dir= s_ref_genome_dir,
                fasta_file= s_ref_fasta_file ,  
                gtf_file= s_ref_gtf_file)

        self.tmp_provider= TmpProvider(root_dir= tmp_root_dir)
        self.alignment_root_dir= os.path.join(self.output_root_dir, "alignment")


    def get_alignment_provider(self, aln_name):
        return AlignmentProvider(self.alignment_root_dir, aln_name)
    
    def get_alignment_tmp_provider(self, aln_name):
        return AlignmentTmpProvider(tmp_root_dir, aln_name)

    def refresh_tmp(self):
        self.tmp_provider = TmpProvider(root_dir= tmp_root_dir)





