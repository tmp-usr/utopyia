import glob
import subprocess
import os, sys
import logging


class RNASeqRunner(object):
    def __init__(self, sample_name, fastq_pair1, fastq_pair2, output_dir, remove_inputs= True):
        ### running the batch job
        self.slurm_output_file= os.path.join(output_dir, "kallisto_%s.out" %sample_name)
        self.batch_line = "sbatch --output=%s tintinJob.kallisto.quant.new.GRCh38.sh %s %s %s %s" %(self.slurm_output_file, fastq_pair1, fastq_pair2, sample_name, output_dir)
        
        self.set_logger()
        self.run()

        #if remove_inputs:
            ### log
            #self.logger.debug("Removing decompressed fastq pairs!!!") 
            #os.remove(fastq_pair1)
            #os.remove(fastq_pair2)
        
    def run(self):
        p = subprocess.Popen(self.batch_line, shell=True, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        ### log
        self.logger.debug(out)


    def set_logger(self):
        self.logger= logging.getLogger("rnaseq.rnaseq_runner.RNASeq_Runner")
        self.logger.setLevel(logging.DEBUG)




