import os
import shutil
import subprocess

class ConcatenateCompressed(object):
   
    def __init__(self, compressed_file_paths, root_dir, sample_name, merged_file_name, keep_originals = True):
        
        self.compressed_file_paths= compressed_file_paths
        self.keep_originals= keep_originals
        self.merge_dir= os.path.join(root_dir, sample_name, "merged")
        self.merged_file_path= os.path.join(self.merge_dir, merged_file_name)
        self.create_merge_dir()
        self.concat()
    
    def create_merge_dir(self):

        #if os.path.exists(self.merge_dir):
        #    shutil.rmtree(self.merge_dir)
        if not os.path.exists(self.merge_dir):
            os.makedirs(self.merge_dir)




    def concat(self, bash= True): 
        """
        bash_based: fastest and the most memory efficient
        1. cat file1.gz file2.gz file3.gz > allfiles.gz
        
        gz: did not work
        2. zcat a.gz b.gz | gzip -c > c.txt.gz

        """
        
        if not bash:
            with open(self.merged_file_path, 'wb') as merged_file:
                for file_path in self.compressed_file_paths:
                    with open(file_path, "rb") as f: 
                        merged_file_.write(f.read())    
       
        else:
            pass
        #    command_line= "cat %s > %s" %(" ".join(self.compressed_file_paths), self.merged_file_path)
        #    p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
        #    out, err = p.communicate()
        
        if not self.keep_originals:
            for f in self.compressed_file_paths:
                os.remove(f)

        return self.merged_file_path
    
