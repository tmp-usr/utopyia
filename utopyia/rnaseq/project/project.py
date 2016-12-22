import glob
import os
import sys
from collections import OrderedDict

sys.path.append("../")

from project_objects import Sample, Replicate, Lane, FastQContainer
from fastq.file_learner import FastQFileLearner

import pdb

class Project(object):
    """
        replication_level= sample | replicate | lane
    """

    def __init__(self, name, root_dir, replication_level= "replicate", 
            fname_column_separator="_", fname_read_index=-1, 
            fname_order_index=0, fname_extension=".fastq.gz"):
        
        self.learner= FastQFileLearner(fname_column_separator, fname_read_index, fname_order_index, fname_extension)
        
        self.name= name
        self.root_dir = root_dir
        self.replication_level = replication_level
        self.samples=[]
        
        self.all_fastq_containers= {}
        self.new_fastq_containers= {}
        
        self.trashed_fastq_container= {}
        
        
        
    def update_fastq_containers(self, container_name, dirpath):
        
        if container_name not in self.new_fastq_containers:
            self.new_fastq_containers[container_name] = FastQContainer(container_name, dirpath)

    def populate_fastq_containers(self):
        
        basedir, dirs, files= os.walk(self.root_dir).next()
        
        if self.replication_level == "sample":
            fastq_container_name= basedir
            s= Sample(fastq_container_name, os.path.basename(basedir),
                   fastq_files= glob.glob(os.path.join(basedir, "*%s" %self.learner.fname_extension)))
            self.samples.append(s)
            self.all_fastq_containers[fastq_container_name] = s


        elif self.replication_level == "replicate":
            for sample_name in dirs:
                sample_dir= os.path.join(basedir, sample_name)
                s = Sample(sample_name, sample_dir,
                    fastq_files= glob.glob(os.path.join(sample_dir, 
                        "*%s" %self.learner.fname_extension)),                     
                         learner= self.learner)
                self.samples.append(s)
                fastq_container_name= sample_name
                self.all_fastq_containers[fastq_container_name] = s

        elif self.replication_level == "lane":
            for sample_name in dirs:
                sample_dir= os.path.join(basedir, sample_name)
                sample_dir, replicate_dirs, files= os.walk(sample_dir).next()

                s=Sample(sample_name, sample_dir)
                for replicate_name in replicate_dirs:
                    replicate_dir= os.path.join(sample_dir, replicate_name)
                    r= Replicate(name= '%s_%s' %(sample_name, replicate_name), 
                        dirpath= replicate_dir, fastq_files= glob.glob(
                        os.path.join(replicate_dir, "*%s" %self.learner.fname_extension)), 
                        learner= self.learner
                        )
                    s.replicates.append(r)
                    fastq_container_name= "%s_%s" %(sample_name, replicate_name)
                    self.all_fastq_containers[fastq_container_name] = r 
                self.samples.append(s)
       
        self.current_fastq_containers= self.all_fastq_containers

    def get_fastq_pairs_by_container(self, container):
        """
            order id is the field in the file name which distinguises the pairs
            from each other.
        
        """
        return container.pairs 








#fcm= FastQContainerMerger(rep, ".")
#fcm.merge_container()

