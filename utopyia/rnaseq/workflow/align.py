import sys
sys.path.append("../")

from task import Task, TaskIOProvider
from alignment.aligner import Aligner

from config.task_io import gen_align_io


class AlignIOProvider(TaskIOProvider):
    def __init__(self, root_dir, input_files, output_dirs, output_files, **kwargs):
        TaskIOProvider.__init__(self, root_dir= root_dir, 
                                input_files= input_files,
                                output_dirs= output_dirs,
                                output_files= output_files)
                                                    

class Align(Task):
    def __init__(self, fastq_container, reads1_path, reads2_path, file_learner,
                     method= "kallisto",  log_message="", **kwargs):
        
        align_io= gen_align_io(method, fastq_container, 
                reads1_path, reads2_path, file_learner)
        align_io_provider= AlignIOProvider(**align_io)
        
        Task.__init__(self, align_io_provider, log_message)
        
        self.name= fastq_container.name + "_" +file_learner.trim_extension()
        self.method= method

    def run(self):
        input_params= self.io_provider.input_provider
        output_params= self.io_provider.output_provider
        tmp_params= self.io_provider.tmp_provider
        
        reads1= input_params.reads1.path
        reads2= input_params.reads2.path
        
        alignment_output_dir= output_params.output_dir.path
        ### kallisto specific params
        if self.method == "kallisto":
            genome_index= input_params.genome_index.path
            
            aligner= Aligner(genome_index= genome_index, 
                             output_dir= alignment_output_dir,
                             reads1= reads1, reads2= reads2)
        
        ### star specific params
        elif self.method == "star":

            genome_dir1= input_params.genome_dir1.path 
            genome_dir2= tmp_params.genome_dir2.path
            genome_fasta_path= input_params.genome_fasta_path.path
            
            tmp_output_dir1= tmp_params.tmp_output_dir1.path
            tmp_output_dir2= tmp_params.tmp_output_dir2.path
            
            sj_out= output_params.sj_out.path
            sam_out= output_params.sam_out.path
            gtf_file= output_params.gtf_file.path
            count_out= output_params.count_out.path

            output_prefix= output_params.output_prefix

            aligner= Aligner(genome_dir1= genome_dir1, genome_dir2= genome_dir2,
                             genome_fasta_path= genome_fasta_path, 
                             tmp_output_dir1= tmp_output_dir1,
                             tmp_output_dir2= tmp_output_dir2,
                             sj_out= sj_out, sam_out= sam_out, # this might be bam!!!
                             count_out= count_out, gtf_file= gtf_file, 
                             output_prefix= output_prefix)

        aligner.align(method= self.method)

