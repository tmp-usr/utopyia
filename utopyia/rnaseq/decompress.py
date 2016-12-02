import os

import luigi
from dependencymixin import DependencyMetaTask


class Decompress(DependencyMetaTask):
    #### parameters
    compression_type= luigi.Parameter()
    compressed_fastq_path= luigi.Parameter()
    decompression_dir= luigi.Parameter()

    ##### TODO Check how to assign boolean variables in luigi
    run_bash= luigi.BooleanParameter()
    keep_original= luigi.BooleanParameter()
    
    slurm_output_file= "slurm_outputs/decompression.out"

    
    def output(self):
    
        compression_type= self.get_input('compression_type')
        compressed_fastq_base= os.path.basename(self.get_input('compressed_fastq_path)')
        decompressed_fastq_base= compressed_fastq_base.rstrip(compression_type)
        decompression_dir = self.get_input('decompression_dir')
        decompressed_fastq_path= os.path.join(decompression_dir, decompressed_fastq_base)

        return {
                "decompressed_fastq_path": luigi.LocalTarget(decompressed_fastq_path)
               }

        
    def decompress(self):
        
        compressed_fastq_path= self.get_input("compressed_fastq_path")
        decompressed_fastq_path= self.output()["decompressed_fastq_path"]
        
        compression_type= self.get_input("compression_type")
        
        if compression_type == ".gz":
            with gzip.open(compressed_fastq_path, "rb") as compressed_fastq_file:
                with open(decompressed_fastq_path, "wb") as fastq_file:
                    fastq_file.write(content= compressed_fastq_file.read())
        
        elif compression_type == ".bz":
            
            compressed_fastq_file = BZ2File(compressed_fastq_path)
            with open(self.fastq_file_path, mode= "w")  as fastq_file:
                fastq_file.writelines(compressed_fastq_file.read())


        keep_original= self.get_input('keep_original')
        if not keep_original:
            os.remove(compressed_fastq_path)
    
    
    
    def decompress_bash(self):
        
        compression_type= self.get_input("compression_type")
        
        if compression_type == ".gz":
            decompress_script_path= "./scripts/decompress_gz.sh"
        
        elif compression_type == "bz":
            decompress_script_path= "./scripts/decompress_bz.sh"
                
        compressed_fastq_path= self.get_input("compressed_fastq_path")
        decompressed_fastq_path= self.output()["decompressed_fastq_path"]

        command_line= "sbatch --output=%s %s %s %s" %(self.slurm_output_file, 
                decompress_script_path, compressed_fastq_path, decompressed_fastq_path)
        
        p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        ### log

    
    def run(self):
        run_bash= self.get_input("run_bash")
        if run_bash:
            self.decompress_bash()
        
        else:
            self.decompress()


