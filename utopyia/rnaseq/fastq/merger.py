import os
import shutil
import subprocess
from operator import itemgetter

import pdb

class FastQMerger(object): 
    def __init__(self, file_paths, merged_file_path, keep_originals = True):        
        self.file_paths= file_paths
        self.keep_originals= keep_originals
        self.merged_file_path= merged_file_path #os.path.join(self.merge_dir, merged_file_name)

    def __str__(self): return self.merged_file_path
    def __repr__(self): return self.merged_file_path

    def merge(self, bash= True): 
        """
        bash_based: fastest and the most memory efficient
        1. cat file1.gz file2.gz file3.gz > allfiles.gz
        
        gz: did not work
        2. zcat a.gz b.gz | gzip -c > c.txt.gz

        """
        
        if not bash:
            with open(self.merged_file_path, 'wb') as merged_file:
                for file_path in file_paths:
                    with open(file_path, "rb") as f: 
                        merged_file_.write(f.read())    
        else:
        #    pass
            command_line= "cat %s > %s" %(" ".join(self.file_paths), self.merged_file_path)
            p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
            out, err = p.communicate()
        
        if not self.keep_originals:
            for f in self.compressed_file_paths:
                os.remove(f)



class FastQContainerMerger(object):
    """
        returns a new container.
    """
    def __init__(self, container, merge_dir):
        self.container = container
        self.merge_dir= merge_dir

    
    def merge_container(self):
        pairs1= map(itemgetter(0), self.container.pairs.values())
        pairs2= map(itemgetter(1), self.container.pairs.values())
    
        f_cols1= os.path.basename(pairs1[0]).split(self.container.learner.fname_column_separator)
        f_cols1.pop(self.container.learner.fname_order_index)
            
        f_cols2= os.path.basename(pairs2[0]).split(self.container.learner.fname_column_separator)
        f_cols2.pop(self.container.learner.fname_order_index)
             
        merged_name1 =  self.container.learner.fname_column_separator.join(f_cols1)
        merged_name2 =  self.container.learner.fname_column_separator.join(f_cols2)
        
        merged_path1= os.path.join(self.merge_dir, merged_name1)
        merged_path2= os.path.join(self.merge_dir, merged_name2)
        
        FastQMerger(pairs1, merged_path1).merge()
        FastQMerger(pairs2, merged_path2).merge()
        
        return (merged_path1, merged_path2)
        


