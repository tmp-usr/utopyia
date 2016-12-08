class FileProvider(dict):
    
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        
        self._dict= dict()

        self._dict["raw"] = {
                
                'root_dir':
                    
                }
    
        
        self._dict["reference"]= {
                
                'genome_dir':
                'fasta_file':
                'gtf_file':
                
                }
    


        self._dict["alignment_output"]= {
                
                'sam_file':
                'aligner_specific_output_dir':
                'count_file':
                'tpm_file':
                'fpkm_file':
                
                }


        self._dict["tmp"]= {
                

                'merge_split_dir':
                'decompressed_fastq_dir':
                'reindexed_genome_dir':
                 
                }
        
