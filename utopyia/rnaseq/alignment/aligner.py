import sys
sys.path.append("../")

from star_runs import star_pass_1, star_pass_2, star_pass_3, generate_counts
from kallisto_runs import kallisto_run

from slurm import Slurm
from config.task_params import job_id, resource_type, n_resource, \
                               run_time , job_name ,e_mail        


class Aligner(object):
    """
        Current alignment tool is STAR. Other option is kallisto.
    
    usage:
        Aligner(fastq_pair, genome_dir1="", genome_dir2="", genome_fasta_path="", 
                sjdb_file_chr_start_end="", sam_out="", gtf_out="", 
                count_out= "")

    """
    def __init__(self, reads1, reads2, *args, **kwargs):
        self.reads1= reads1
        self.reads2= reads2
        self.init_attr(**kwargs)
        #self.aligner_path= "/sw/mf/milou/bioinfo-tools/pipeline" 


    def init_attr(self, **kwargs):
       
        if "genome_index" in kwargs:
            self.genome_index = kwargs["genome_index"]

        if "genome_dir1" in kwargs:
            self.genome_dir1= kwargs["genome_dir1"] 

        if "genome_dir2" in kwargs:
            self.genome_dir2= kwargs["genome_dir2"]
 
        if "genome_fasta_path" in kwargs:
            self.genome_fasta_path= kwargs["genome_fasta_path"]

        if "sj_out" in kwargs:
            self.sj_out= kwargs["sj_out"]

        if "tmp_output_dir1" in kwargs:
            self.tmp_output_dir1= kwargs["tmp_output_dir1"]


        if "tmp_output_dir2" in kwargs:
            self.tmp_output_dir2= kwargs["tmp_output_dir2"]

        if "sam_out" in kwargs:
            self.sam_out = kwargs["sam_out"]

        if "gtf_file" in kwargs:
            self.gtf_file= kwargs["gtf_file"]

        if "count_out" in kwargs:
            self.count_out= kwargs["count_out"]

        if "output_prefix" in kwargs:
            self.output_prefix = kwargs["output_prefix"]
            
        if "output_dir" in kwargs:
            self.output_dir = kwargs["output_dir"]
            
    def align(self, method= "star"):
        
        print method
        if method == "star":
            command_line_1 = star_pass_1(self.genome_dir1, self.reads1, self.reads2, self.tmp_output_dir_1, self.output_prefix)
            command_line_2 = star_pass_2(self.genome_dir2, self.genome_fasta_path, self.sj_out)
            command_line_3 = star_pass_3(self.genome_dir2, self.reads1, self.reads2, self.tmp_output_dir_2, self.output_prefix)
            command_line_4 = generate_counts(self.sam_out, self.gtf_file, self.count_out)

    
            command_line= "\n".join([command_line_1, command_line_2, command_line_3, command_line_4])

            
            print Slurm(job_id, resource_type= resource_type, n_resource = n_resource,
                    run_time= run_time, job_name= job_name, 
                    email= e_mail, command_line= command_line_1)
            print Slurm(job_id, resource_type= resource_type, n_resource = n_resource,
                    run_time= run_time, job_name= job_name, 
                    email= e_mail, command_line= command_line_2)
            print Slurm(job_id, resource_type= resource_type, n_resource = n_resource,
                    run_time= run_time, job_name= job_name, 
                    email= e_mail, command_line= command_line_3)
            print Slurm(job_id, resource_type= resource_type, n_resource = n_resource,
                    run_time= run_time, job_name= job_name, 
                    email= e_mail, command_line= command_line_4)
            
        elif method == "kallisto":
            command_line = kallisto_run(self.genome_index, self.output_dir, self.reads1, self.reads2)
            print Slurm(job_id, resource_type= resource_type, n_resource = n_resource,
                    run_time= run_time, job_name= job_name, 
                    email= e_mail, command_line= command_line)

