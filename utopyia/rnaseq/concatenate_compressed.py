
class ConcatenateCompressed(DependencyMetaTask):
    
    compressed_file_paths= luigi.ListParameter()
    merged_file_path= luigi.ListParameter()
    keep_original= luigi.BooleanParameter()

    def output(self):
        return {'merged_file_path': self.get_input("merged_file_path")}


    def concatenate_inputs(self, bash= True):
        
        """
        bash_based: fastest and the most memory efficient
        1. cat file1.gz file2.gz file3.gz > allfiles.gz
        
        gz: did not work
        2. zcat a.gz b.gz | gzip -c > c.txt.gz

        """
        
        compressed_file_paths= self.get_input('compressed_file_paths')
        merged_file_path= self.get_input("merged_file_path") 
        
        if not bash:
            with open(merged_file_path, 'wb') as merged_file:
                for file_path in compressed_file_paths:
                    with open(file_path, "rb") as f: 
                        merged_file_file.write(f.read())    
            
        else:
            command_line= "cat %s > %s" %(" ".join(compressed_file_paths), merged_file_path)
            p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
            out, err = p.communicate()

    
    def run(self):
        self.concatenate_inputs()
    

