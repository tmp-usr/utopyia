import os
import shutil
import glob
import subprocess

from janitor.batch_reader import BatchReader
from memory_profiler import profile

#gzip_files= glob.glob("../test_data/*_1.fastq.gz")
gzip_files= glob.glob("../compressed_fastq_data/*_1.fastq.gz")

print gzip_files
#gzip_files= ["../test_data/reads.fastq"]

bzip_files= []

gzip_file=""
bzip_file=""

decompressed_file = "../test_outputs/reads_1.fastq.gz"

bash_gz_decompression_command= ""
bash_bz_decompression_command= ""


def test_decompression():
    pass


def test_bash_decompression(decompression_type= ".gz"):
    if decompression_type == ".gz":
        pass

    elif decompression_type == ".bz":
        pass


@profile
def test_concatenation(): 
    """
        3218381 function calls in 5.001 seconds
    """
    
    file_list = gzip_files
    dest_filename = decompressed_file

    buffer_size = 10000000  # Adjust this according to how "memory efficient" you need the program to be.
    with open(dest_filename, 'wb') as dest_file:
        for file_name in file_list:
            br= BatchReader( buffer_size, iterator= open(file_name))
            for chunk in br: 
                for line in chunk:
                    dest_file.write(line)
                
#@profile
def test_concatenation2(): 
    """
        10 function calls in 3.006 seconds
    """
    
    file_list = gzip_files
    dest_filename = decompressed_file

    with open(dest_filename, 'wb') as dest_file:
        for file_name in file_list:
            with open(file_name, "rb") as f: 
                dest_file.write(f.read())

#@profile
def test_bash_concatenation():
    #bash_based
    """
        cat: 39 function calls in 2.192 seconds
        zcat: could not recognize fastq.gz files. 
    """
    #command_line= "zcat %s |gzip -c > %s" %(" ".join(gzip_files), decompressed_file)

    command_line= "cat %s > %s" %(" ".join(gzip_files), decompressed_file)
    
    p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    


#test_bash_concatenation()

import cProfile
cProfile.run('test_concatenation2()')

