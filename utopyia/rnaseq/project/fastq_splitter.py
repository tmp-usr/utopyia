import os
import subprocess
import gzip
import shutil

from janitor.batch_reader import BatchReader

from fastq_parser import FastQParser


from multiprocessing import Pool

class FastQSplitter(object):
    def __init__(self, file_path, root_dir, sample_name, compressed= True, n_seq= 1000):
        
        self.file_path= file_path
        split_basename= "%s_sp" % os.path.basename(file_path).replace(".fastq.gz","")
        self.split_dir= os.path.join(root_dir, sample_name, "split", split_basename)

        self.split_prefix= os.path.basename(self.file_path).replace(".fastq.gz","")
        self.split_fastq_files= []
        self.compressed= compressed
        self.n_seq= n_seq

        self.create_split_dir()


    def run(self):
        if self.compressed:
            return self.split_compressed(True)
        else:
            return self.split()


    def create_split_dir(self):
        ### 
        if os.path.exists(self.split_dir):
            shutil.rmtree(self.split_dir)
        

        #### When the jobs are parallelyzed this might be
        #### meaningful
        if not os.path.exists(self.split_dir):
            os.makedirs(self.split_dir)

    
    
    def split_compressed(self, decompress= False):
        """
            BZ2 support will be added. Currently only works for gzipped fastq files.
        """
        #n_lines= self.total_lines_compressed        
        #n_line_per_file= n_lines / 4 / self.split_times 

        ### count the total lines in a compressed file
        handle= gzip.open(self.file_path, "rb")
        seq_handle= FastQParser(handle).fastq_sequences
       

        br= BatchReader(self.n_seq ,seq_handle)
    
        for i, chunk in enumerate(br, 1):
            if decompress:
                split_fastq_path= os.path.join(self.split_dir, "%s_%d.fastq" % (self.split_prefix, i))
                split_fastq= open(split_fastq_path, "w") 

            else:

                split_fastq_path= os.path.join(self.split_dir, "%s_%d.fastq.gz" % (self.split_prefix, i))
                split_fastq= gzip.open(split_fastq_path, "w") 
                    
            split_fastq.write("".join(str(seq) for seq in chunk))
            split_fastq.close()
            yield split_fastq_path

 


    def split(self):

        n_seqs= self.total_lines / 4
        n_seq_per_file= n_seqs / self.split_times 
        n_line_per_file= n_seq_per_file * 4
    
        with open(self.file_path) as fastq_file:
            all_lines= fastq_file.readlines()
            f_contents = [all_lines[i*n_line_per_file:(i+1)*n_line_per_file] for i in range(self.split_times)]
            
            f_contents[-1]= all_lines[(self.split_times-1) * n_line_per_file:]
            
            for i, fastq_lines in enumerate(f_contents):
                fastq_i_path= os.path.join(self.split_dir, "%d.fastq" % (i+1))
                if fastq_lines != []:
                    with open(fastq_i_path,"w") as fastq_i:
                        fastq_i.write("".join(fastq_lines))
                    self.split_fastq_files.append(fastq_i_path)            

        return self.split_fastq_files


    @property
    def total_lines(self):
        """
            Thanks to the github user sed for sharing the following link.
            https://gist.github.com/zed/0ac760859e614cd03652
        """
        p = subprocess.Popen(['wc', '-l', self.file_path], stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        
        return int(result.strip().split()[0])

    @property
    def total_lines_compressed(self):
        """
            total number of lines in one of the colon cancer rna seq data: 36757144

        """
        command_line1=  "zgrep -Ec '$' %s" % os.path.abspath(self.file_path)
        p = subprocess.Popen(command_line1, shell=True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        n_lines, err = p.communicate()
        return int(n_lines)
        
    

trash = """
        command_line1=  "zgrep -Ec '$' %s" % os.path.abspath(self.file_path)
        p = subprocess.Popen(command_line1, shell=True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        n_lines, err = p.communicate()
        n_lines= int(n_lines)
        n_line_per_file= n_lines / 4 / (self.split_times - 1) * 4 
        
        if bash:
            ### split the files in lines of split_times
            command_line2 = "zless %s |split -l %d - %s" %(self.file_path, n_line_per_file,  os.path.basename(self.file_path)) 
            p = subprocess.Popen(command_line2, shell= True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        else:
            with gzip.open(self.file_path, 'rb') as inp:
                
                for i in range(self.split_times):
                    fastq_i_path= os.path.join(self.split_dir, "%d.fastq.gz" % (i+1))
                    with gzip.open(fastq_i_path,'wb') as outp:
                        outp.write(inp.read(n_line_per_file))
"""

trash="""
    
    j= 0
    for i, seq in enumerate(seq_handle):
        if i % n_line_per_file == 0:
            j+=1
            if j <= self.split_times:
                
                if decompress:
                    split_fastq_path= os.path.join(self.split_dir, "%s_%d.fastq" % (self.split_prefix, j))
                    split_fastq= open(split_fastq_path, "w") 
                
                else:
                    split_fastq_path= os.path.join(self.split_dir, "%s_%d.fastq.gz" % (self.split_prefix, j))
                    split_fastq= gzip.open(split_fastq_path, "wb")
                
                self.split_fastq_files.append(os.path.abspath(split_fastq_path))            
            if i > 0:
                yield split_fastq_path
        
        split_fastq.write(str(seq))
            
    ### yield the last file
    yield split_fastq_path
         
    #return self.split_fastq_files
    """
