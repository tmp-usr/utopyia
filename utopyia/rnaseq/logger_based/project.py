import glob
import os




class Project(object):
    """
        replication_level= sample | replicate | lane
    """

    def __init__(self, name, dirpath, replication_level= "replicate"):
        self.name= name
        self.dirpath = dirpath
        self.replication_level = replication_level
        self.samples=[]
    
        
        
    def populate_samples(self):
        basedir, dirs, files= os.walk(self.dirpath).next()
        
        if self.replication_level == "sample":
            s= Sample(base_dir, os.path.basename(basedir),
                   fastq_files= glob.glob(os.path.join(basedir, "*.fastq.gz")))
            self.samples.append(s)


        elif self.replication_level == "replicate":
            for sample_dir in dirs:
                sample_dir, replicate_dirs, files= os.walk(sample_dir)
                s = Sample(os.path.basename(sample_dir), sample_dir,
                    fastq_files= glob.glob(os.path.join(sample_dir, "*.fastq.gz")))
            
        elif self.replication_level == "lane":
            for sample_dir in dirs:
                sample_dir, replicate_dirs, files= os.walk()
                s=Sample(os.path.basename(sample_dir), sample_dir)
                for replicate_dir in replicate_dirs:
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

base_dir= "/Users/kemal/shared/github_repos/utopyia/utopyia/rnaseq/test_data"
sample_level_path= os.path.join(base_dir, "mock_project_sample_level")

p= Project("pr_sample", sample_level_path, replication_level= "sample")

p.populate_samples()


