import os

from project_learner import ProjectLearner
from fastq_decompressor import FastQDecompressor
from rnaseq_runner import RNASeqRunner


class Controller(object):
    def __init__(self, project_dir, decompression_dir, output_dir, log_dir):
        self.log_dir= log_dir
        self.project_dir= project_dir
        self.output_dir= output_dir
        self.decompression_dir= decompression_dir
        
        self.project_learner= ProjectLearner(project_dir)


    def concatenate_files(self, files):
        """
            concatenates fastq files into one and deletes the originals
        """
        new_file_name= os.path.join(os.path.dirname(files[0]), "_".join(os.path.basename(files[0]).split("_")[1:]))
        print new_file_name
        buffer_size= 1000
        with open(new_file_name, "w") as new_file:
            print new_file_name
            for f in files:
                with open(f, "rb") as f_read:
                    chunk= True
                    while chunk:
                        chunk = f_read.read(buffer_size)
                        new_file.write(chunk)    
                   
                   

    def decompress(self):
        i= 2
        for sample_dir, replicate_dir, replicate in self.yield_lane_pairs():
            pair_1_files= []
            pair_2_files= []
            for lane_pairs in replicate:
                lane= lane_pairs[0]
                pair1= lane_pairs[1][0]
                pair2= lane_pairs[1][1]

                decompressor_1= FastQDecompressor(pair1, self.decompression_dir, output_dir= self.log_dir)
                decompressor_2= FastQDecompressor(pair2, self.decompression_dir, output_dir= self.log_dir)
                
                #print pair1
                #print pair2
                #print
                fastq_1= decompressor_1.fastq_file_path
                fastq_2= decompressor_2.fastq_file_path
                
                pair_1_files.append(fastq_1)
                pair_2_files.append(fastq_2)
                

                try:
                    RNASeqRunner(self, sample_dir, pair1, pair2, self.output_dir)
                
                except Exception, e:
                    print e
                    pass
            
            #self.concatenate_files(pair_1_files)
            #self.concatenate_files(pair_2_files)



                #iprint fastq_1
                #print fastq_2
                #print
                #i+=1
                #if i == 2:
                #    break 
            #break


project_dir= "/proj/b2014274/INBOX/F.Ponten_16_01"
decompression_dir= "/home/adilm/projects/colon_cancer"
log_dir= "/home/adilm/projects/colon_cancer/log"
output_dir= "/home/adilm/projects/colon_cancer/outputs"

c= Controller(project_dir, decompression_dir, output_dir, log_dir)
c.decompress()

