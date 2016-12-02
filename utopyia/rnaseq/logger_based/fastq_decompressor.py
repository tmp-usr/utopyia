import logging
import os
import subprocess

from bz2 import BZ2File 


class FastQDecompressor(object):
    """
        accepts a compressed fastq file input and yields a 
        decompressed version in the same directory.
    """
    
    def __init__(self, compressed_fastq_file_path, decompression_dir=".", output_dir= ".", keep_original= True, compression_type= ".gz", sample_name= "", replicate_name= ""):
        
        self.compressed_fastq_file_path = compressed_fastq_file_path
        fastq_base= os.path.basename(self.compressed_fastq_file_path.rstrip(compression_type))
        self.fastq_file_path= os.path.join(decompression_dir, sample_name, replicate_name, fastq_base)
        self.decompression_dir= decompression_dir
        self.output_dir= output_dir
        self.compression_type= compression_type


        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        
        self.slurm_output_file= os.path.join(self.output_dir, fastq_base) + ".out"   
        self.keep_original = keep_original
        

        self.set_logger()
        ### log
        #self.decompress_alt()
    
    def set_logger(self):
        self.logger= logging.getLogger("rnaseq.fastq_decompressor.FastQDecomompressor")
        self.logger.setLevel(logging.DEBUG)


    def decompress_alt(self):
        command_line= "sbatch --output=%s decompress.sh %s %s" %(self.slurm_output_file, self.compressed_fastq_file_path, self.fastq_file_path)
        p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        ### log
        self.logger.debug(out)

        self.logger.debug("Decompression submitted!")
        return self.fastq_file_path

    
    def decompress_bzip(self):
        compressed_fastq_file = BZ2File(self.compressed_fastq_file_path)
        fastq_file= open(self.fastq_file_path, mode= "w")
            
        fastq_file.writelines(compressed_fastq_file.read())
    
        if not self.keep_original:
            os.remove(self.compressed_fastq_file_path)
    
        return self.fastq_file_path


    def decompress_gzip(self):
        with gzip.open(self.compressed_fastq_file_path, "rb") as compressed_f:
            with open(self.fastq_file_path, "wb") as fastq_file:
                fastq_file.write(content= compressed_f.read())
                
        if not self.keep_original:
            os.remove(self.compressed_fastq_file_path)
    
        return self.fastq_file_path

