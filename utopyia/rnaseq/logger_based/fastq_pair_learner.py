import glob,os
#learner
class FastQPairLearner(object):
    """
        RNASeqPairLearner class is specifically written for 
        the compressed fastq files retrieved from GATC. File 
        names include project id, sample id and pair id. 
        
    """
    
    def __init__(self, input_dir, compression_format="bz2"):
        
        self.input_dir= input_dir
        self.compression_format= compression_format
        
        self.input_files= glob.glob(os.path.join(self.input_dir, 
            "*.%s" % compression_format))
        
    def yield_pairs(self):
        for absolute_file_path in self.input_files:
            compressed_fastq_base= os.path.basename(absolute_file_path)
            compressed_fastq_dir= os.path.dirname(absolute_file_path)

            f_sp= compressed_fastq_base.rsplit("_",1)
            
            sample_name= compressed_fastq_base.split("_lib")[0].split('_',1)[1]

            pair_ext= f_sp[1].split('.',1)
            
            pair_no= pair_ext[0]    

            if pair_no == str(2):
                continue

            prepath= f_sp[0]
            pairs = [os.path.join(compressed_fastq_dir, 
                        prepath+"_"+str(pair_no)+".fastq."+self.compression_format) 
                        for pair_no in (1,2)]
            yield sample_name, (os.path.join(compressed_fastq_dir, pair) for pair in pairs)

