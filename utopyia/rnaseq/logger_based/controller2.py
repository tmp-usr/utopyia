import os, logging
import time
import subprocess

from fastq_pair_learner import FastQPairLearner
from fastq_decompressor import FastQDecompressor
from rnaseq_runner import RNASeqRunner

#SLURM_OUT_FILE = "slurm.out"

class Controller(object):
    def __init__(self, compressed_input_dir, fastq_input_dir, output_dir):
        self.fastq_pair_learner= FastQPairLearner(compressed_input_dir)     
        self.fastq_input_dir= fastq_input_dir
        self.output_dir= output_dir

        
        self.current_fastq_pair1_file_path= ""
        self.current_fastq_pair2_file_path= ""

        
        self.set_logger()
        self.create_dirs()
       

        self.run()
    

    def create_dirs(self):
        ### log        
        self.logger.debug("Creating directory %s" % self.fastq_input_dir)
        if not os.path.exists(self.fastq_input_dir):
            os.makedirs(self.fastq_input_dir)


    def set_logger(self):
        # create logger with "spam application"
        self.logger= logging.getLogger('rnaseq')
        self.logger.setLevel(logging.DEBUG)

        # create a file handler 
        fh= logging.FileHandler("run_seq_runner.log", mode= "w")
        fh.setLevel(logging.INFO)

        # create a console handler
        ch= logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # set formatter
        #formatter = logging.Formatter("%(asctime)s - %(name)s- %(levelname)s - %(message)s", 
        #        datefmt='%m/%d/%Y %I:%M:%S %p')
        
        formatter = logging.Formatter("%(asctime)s - %(message)s")
               
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def check_job_status(self, job_name, slurm_outputs, batch_submission_wait= 5, job_running_wait= 5):
        self.logger.debug("Submitted slurm job. Waiting for allocation of resources!")
        while not all([os.path.exists(slurm_output_file) for slurm_output_file in slurm_outputs]):
            time.sleep(batch_submission_wait)
            self.logger.info("Waiting for allocation of resources.")

        self.logger.debug("Slurm jobs started.")
        
        command_line = 'squeue | grep adilm'
        
        p = subprocess.Popen(command_line, shell=True, stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

        out = p.stdout.read()
        
        
        while out !=  "":
            time.sleep(job_running_wait)
            self.logger.info("%s is still running. Please wait!" % job_name)
           
            p = subprocess.Popen(command_line, shell=True, stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

            out = p.stdout.read()

        self.logger.debug(" %s runs are finished!" % job_name)


    def run(self):
        ### log 
        self.logger.debug("RNA-Seq pipeline started!") 
        i= 0
        
        decompressor_outputs= []
        for sample_name, compressed_fastq_pair in self.fastq_pair_learner.yield_pairs():
            
            self.sample_name= sample_name
            compressed_fastq_pair= list(compressed_fastq_pair)
            
            sample_output_dir = self.output_dir + "_" + sample_name
            
            self.current_fastq_pair1_file_path = compressed_fastq_pair[0]
            self.current_fastq_pair2_file_path = compressed_fastq_pair[1]
            
            decompressor1= FastQDecompressor(self.current_fastq_pair1_file_path, decompression_dir= self.fastq_input_dir, output_dir= sample_output_dir)
            decompressor1.decompress_alt()
            #self.fastq_pair1= decompressor1.fastq_file_path
            
            decompressor2= FastQDecompressor(self.current_fastq_pair2_file_path, decompression_dir= self.fastq_input_dir, output_dir= sample_output_dir)
            decompressor2.decompress_alt()
            #self.fastq_pair2= decompressor2.fastq_file_path
            
            decompressor_outputs.append(decompressor1.slurm_output_file)
            decompressor_outputs.append(decompressor2.slurm_output_file)
            
            i+=1
            #if i == 1:
            #    break

        self.check_job_status("Decompression", decompressor_outputs)
        
        kallisto_outputs= []
        i=0
        for sample_name, compressed_fastq_pair in self.fastq_pair_learner.yield_pairs():
            
            self.sample_name= sample_name
            compressed_fastq_pair= list(compressed_fastq_pair)
            
            sample_output_dir = self.output_dir + "_" + sample_name
            
            self.current_fastq_pair1_file_path = compressed_fastq_pair[0]
            self.current_fastq_pair2_file_path = compressed_fastq_pair[1]
            
            decompressor1= FastQDecompressor(self.current_fastq_pair1_file_path, decompression_dir= self.fastq_input_dir, output_dir= sample_output_dir)
            self.fastq_pair1= decompressor1.fastq_file_path
            
            decompressor2= FastQDecompressor(self.current_fastq_pair2_file_path, decompression_dir= self.fastq_input_dir, output_dir= sample_output_dir)
            self.fastq_pair2= decompressor2.fastq_file_path           
            

            
            rnaseq_runner= RNASeqRunner(sample_name, self.fastq_pair1, self.fastq_pair2, sample_output_dir)
            kallisto_outputs.append(rnaseq_runner.slurm_output_file)

            i+=1
            #if i == 1:
            #    break

        self.check_job_status("Kallisto", kallisto_outputs, job_running_wait= 20)
        
       
        ### log
        self.logger.debug("RNA-Seq pipeline finished!")


#compressed_input_dir= "/Volumes/Samsung_T3/hek293"
#fastq_input_dir= "/Users/kemal/Desktop/postdoc/projects/hek293"
#output_dir= "/Users/kemal/Desktop/postdoc/projects/hek293/outputs"

compressed_input_dir= "/proj/b2016253/hek293"
fastq_input_dir= "/home/adilm/glob/projects/hek293"
output_dir= "/home/adilm/glob/projects/hek293/outputs"

c= Controller(compressed_input_dir, fastq_input_dir, output_dir)

