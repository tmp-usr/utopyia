import os

class ConcatenateCompressed(object):
   
    def __init__(self, compressed_file_paths, merged_file_path, keep_originals = True):
        
        self.compressed_file_paths= compressed_file_paths
        self.merged_file_path= merged_file_path
        self.keep_originals= keep_originals

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
                        merged_file_file.write(f.read())    
            
        else:
            command_line= "cat %s > %s" %(" ".join(self.compressed_file_paths), self.merged_file_path)
            p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
            out, err = p.communicate()
        
        if not self.keep_originals:
            for f in self.compressed_file_paths:
                os.remove(f)

    
