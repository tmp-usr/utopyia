import os
import subprocess
import gzip
import shutil

from itertools import izip
from operator import itemgetter

import io
import StringIO
import tempfile
import bz2
from bz2 import BZ2File
import tarfile

from janitor.batch_reader import BatchReader
from fastq.parser import FastQParser
from multiprocessing import Pool
from decompressor import FastQDecompressor


import pdb

class FastQSplitter(object):
    """
        Since the splitting of big (a few GB) fastq files takes long time,
        the outputs of this class will always be generators to stream them
        into the following task. F

    """
    
    def __init__(self, file_path, split_dir, 
                       compressed= True, n_seq= 1000, 
                       compression_method= "gzip"):
        
        self.file_path= file_path
        
        

        if compression_method == "gzip":
            extension= ".gz"

        elif compression_method == "bzip":
            extension= ".bz2"

        elif compression_method == "tar.gz":
            extension= ".tar.gz"

        #split_basename= "%s_sp" % os.path.basename(file_path).replace(".fastq%s" %extension, "")
        self.split_dir= split_dir #os.path.join(root_dir, sample_name, "split", split_basename)
        self.split_prefix= os.path.basename(self.file_path).replace(".fastq%s" %extension,"")
        self.compressed= compressed
        self.compression_method= compression_method
        self.n_seq= n_seq

        self.split_fastq_files= []
        
    
    def split(self, decompress= True):
        """
            BZ2 support will be added. Currently only works for gzipped fastq files.
        """
        #n_lines= self.total_lines_compressed        
        #n_line_per_file= n_lines / 4 / self.split_times 

        ### count the total lines in a compressed file
        if self.compressed:
            decompressor= FastQDecompressor(self.file_path, self.compression_method, return_type= "stream")
            handle= decompressor.decompress()
        
        else:
            handle= open(self.file_path, "r")


        seq_handle= FastQParser(handle).fastq_sequences
        br= BatchReader(self.n_seq ,seq_handle)
        
        for i, chunk in enumerate(br, 1):
            if decompress or self.compressed == False:
                split_fastq_path= os.path.join(self.split_dir, "%d.fastq" % i)
                split_fastq= open(split_fastq_path, "w") 

            else:
                split_fastq_path= os.path.join(self.split_dir, "%s_%d.fastq.gz" % (self.split_prefix, i))
                split_fastq= gzip.open(split_fastq_path, "w") 
                    
            split_fastq.write("".join(str(seq) for seq in chunk))
            split_fastq.close()

            yield i, split_fastq_path


class FastQContainerSplitter(object):
    def __init__(self, fastq_container, split_dir, n_seq= 1000, compression_method= "gzip"):
        self.fastq_container = fastq_container
        self.split_dir= split_dir
        self.n_seq=n_seq
        self.compression_method= compression_method
#
        
    def split_container(self):
        """
            We will update the all_fastq_containers attribute of the 
            project object with the generated file paths out of this 
            method.

            We need to generate io providers for each directory generated
            in the intermediary steps like this. see the split_dir below.

        """
        new_containers= {}
        old_name= self.fastq_container.name
        
        for pair1, pair2 in self.fastq_container.pairs.values():
            
            self.fastq_container.learner.set_file(pair1)
            fname1=  self.fastq_container.learner.trim_extension()

            self.fastq_container.learner.set_file(pair2)
            fname2= self.fastq_container.learner.trim_extension()
 
            split_dir_name1= fname1
            split_dir_path1= os.path.join(self.split_dir, split_dir_name1)   

            split_dir_name2= fname2
            split_dir_path2= os.path.join(self.split_dir, split_dir_name2)  

            if not os.path.exists(split_dir_path1):
                os.makedirs(split_dir_path1)
            if not os.path.exists(split_dir_path2):
                os.makedirs(split_dir_path2)
            

            split_handle1 = FastQSplitter(pair1, split_dir_path1, compressed= True, 
                    n_seq= self.n_seq, compression_method= self.compression_method).split()
            
            split_handle2 = FastQSplitter(pair2, split_dir_path2, compressed= True, 
                    n_seq= self.n_seq, compression_method= self.compression_method).split()

            if split_dir_name1 not in new_containers:
                new_containers[split_dir_name1] = 1
                self.fastq_container.name = "%s_%s" %(old_name, split_dir_name1.rstrip("_1")) 
            
            yield izip(map(itemgetter(1), split_handle1), map(itemgetter(1), split_handle2))

#### TODO: construct new containers with the new names. the current version is enough to initiate the runs

trash="""
    @property
    def total_lines(self):
        '''
            Thanks to the github user sed for sharing the following link.
            https://gist.github.com/zed/0ac760859e614cd03652
        '''
        p = subprocess.Popen(['wc', '-l', self.file_path], stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        
        return int(result.strip().split()[0])

    @property
    def total_lines_compressed(self):
        '''
            total number of lines in one of the colon cancer rna seq data: 36757144

        '''
        command_line1=  "zgrep -Ec '$' %s" % os.path.abspath(self.file_path)
        p = subprocess.Popen(command_line1, shell=True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        n_lines, err = p.communicate()
        return int(n_lines)
"""



