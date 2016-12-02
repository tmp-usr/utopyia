from fastq_pair_learner import FastQPairLearner
from fastq_decompressor import FastQDecompressor
from rnaseq_runner import RNASeqRunner


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
        for rnaseq_dir in (self.fastq_input_dir, self.output_dir):
            if not os.exists(rnaseq_dir):
                ### log
                self.logger.debug("Creating directory %s" % rnaseq_dir)
                os.makedirs(rnaseq_dir)


    def set_logger(self):
        # create logger with "spam application"
        self.logger= logging.getLogger('rnaseq')
        self.logger.setLevel(logging.DEBUG)

        # create a file handler 
        fh= logging.FileHandler("run_seq_runner.log", mode= "w")
        fh.setLevel(logging.DEBUG)

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


    def run(self):
        ### log 
        self.logger.debug("RNA-Seq pipeline started!") 
        for compressed_fastq_pair in self.fastq_pair_learner.yield_pairs()
            self.current_fastq_pair1_file_path = compressed_fastq_pair[0]
            self.current_fastq_pair2_file_path = compressed_fastq_pair[1]
            
            self.fastq_pair1= FastQDecompressor(self.current_fastq_pair1_file_path, self.fastq_input_dir).decompress()
            self.fastq_pair2= FastQDecompressor(self.current_fastq_pair2_file_path, self.fastq_input_dir).decompress()

            rnaseq_runner= RNASeqRunner(self.fastq_pair1, self.fastq_pair2, self.output_dir)
            rnaseq_runner.run()

        ### log
        self.logger.debug("RNA-Seq pipeline finished!")

compressed_input_dir= "/proj/b2016253/hek293/"
fastq_input_dir= "/home/adilm/glob/projects/hek293"
output_dir= "/home/adilm/glob/projects/hek293/outputs"
c= Controller(compressed_input_dir, fastq_input_dir, output_dir)
