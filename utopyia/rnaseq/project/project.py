import glob
import os

from project_objects import Sample, Replicate, Lane


import pdb

class Project(object):
    """
        replication_level= sample | replicate | lane
    """

    def __init__(self, name, dirpath, replication_level= "replicate"):
        self.name= name
        self.dirpath = dirpath
        self.replication_level = replication_level
        self.samples=[]
    
        self.populate_samples()

        
    def populate_samples(self):
        basedir, dirs, files= os.walk(self.dirpath).next()
        
        if self.replication_level == "sample":
            s= Sample(base_dir, os.path.basename(basedir),
                   fastq_files= glob.glob(os.path.join(basedir, "*.fastq.gz")))
            self.samples.append(s)


        elif self.replication_level == "replicate":
            for sample_name in dirs:
                sample_dir= os.path.join(basedir, sample_name)
                s = Sample(sample_name, sample_dir,
                    fastq_files= glob.glob(os.path.join(sample_dir, "*.fastq.gz")))
                self.samples.append(s)

        elif self.replication_level == "lane":
            for sample_name in dirs:
                sample_dir= os.path.join(basedir, sample_name)
                sample_dir, replicate_dirs, files= os.walk(sample_dir).next()

                s=Sample(sample_name, sample_dir)
                for replicate_name in replicate_dirs:
                    replicate_dir= os.path.join(sample_dir, replicate_name)
                    r= Replicate(os.path.basename(replicate_dir), replicate_dir,
                            fastq_files= glob.glob(os.path.join(replicate_dir, "*.fastq.gz")))
                    s.replicates.append(r)
                self.samples.append(s)
        

    def fastq_pairs(self):
        pass

    def concatenate_replicates(self):
        assert self.replication_level != "lane", "Current replication level is not recommended for concatenation!"

    def decompress_replicates(self):
        pass

    def split_fastq_files(self):
        pass


