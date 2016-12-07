from star_runs import *

from slurm import Slurm


class Aligner(object):
    """
        Current alignment tool is STAR. Other option is kallisto.
    
    usage:
        Aligner(fastq_pair, genome_dir1="", genome_dir2="", genome_fasta_path="", 
                sjdb_file_chr_start_end="", sam_out="", gtf_out="", 
                count_out= "")

    """
    def __init__(self, fastq_pair, *args, **kwargs):
        self.fastq_pair= fastq_pair
        self.init_attr(**kwargs)
        self.aligner_path= "/sw/mf/milou/bioinfo-tools/pipeline" 


    def init_attr(self, **kwargs):
        
        if "genome_dir1" in kwargs:
            self.genome_dir1= kwargs["genome_dir1"] 

        if "genome_dir2" in kwargs:
            self.genome_dir2= kwargs["genome_dir2"]
 
        if "genome_fasta_path" in kwargs:
            self.genome_fasta_path= kwargs["genome_fasta_path"]

        if "sjdb_file_chr_start_end" in kwargs:
            self.sjdb_file_chr_start_end= kwargs["sjdb_file_chr_start_end"]

        if "tmp_output_dir_1" in kwargs:
            self.tmp_output_dir_1= kwargs["tmp_output_dir_1"]


        if "tmp_output_dir_2" in kwargs:
            self.tmp_output_dir_2= kwargs["tmp_output_dir_2"]

        if "sam_out" in kwargs:
            self.sam_out = kwargs["sam_out"]

        if "gtf_out" in kwargs:
            self.gtf_out= kwargs["gtf_out"]

        if "count_out" in kwargs:
            self.count_out= kwargs["count_out"]

        if "output_dir" in kwargs:
            self.output_dir = kwargs["output_dir"]

    def align_fastq_pair(self, aligner= "star"):
        if aligner == "star":
            command_line_1 = star_pass_1(self.genome_dir1, self.fastq_pair, self.tmp_output_dir_1)
            command_line_2 = star_pass_2(self.genome_dir2, self.genome_fasta_path, self.sjdb_file_chr_start_end)
            command_line_3 = star_pass_3(self.genome_dir2, self.fastq_pair, self.tmp_output_dir_2, self.output_dir)


            s1= Slurm("b2016253", resource_type= "core", n_resource = 8, run_time= "00:30:00", 
                                job_name= "test_1", email= "", command_line=command_line_1)
   

            s2= Slurm("b2016253", resource_type= "core", n_resource = 8, run_time= "00:30:00", 
                                job_name= "test_1", email= "", command_line=command_line_2)

            s3= Slurm("b2016253", resource_type= "core", n_resource = 8, run_time= "00:30:00", 
                                job_name= "test_1", email= "", command_line=command_line_3)

