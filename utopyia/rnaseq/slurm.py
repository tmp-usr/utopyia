import tempfile
import subprocess
import os
import pdb

class Slurm(object):
    
    def __init__(self, job_id, resource_type= "core", n_resource = 8, run_time= "00:30:00",
                       job_name= "", email= "", command_line=""):
        self.job_id= job_id
        self.resource_type= resource_type
        self.n_resource= n_resource
        self.run_time= run_time
        self.job_name= job_name
        self.email= email
        self.command_line= command_line
        self.batch() 
    
    def __str__(self):
        return self.content

    
    @property
    def content(self):
        content= """#!/bin/bash -l

#SBATCH -A %s
#SBATCH -p %s
#SBATCH -n %d
#SBATCH -t %s
#SBATCH -J %s
#SBATCH --mail-user %s
#SBATCH --mail-type=ALL

%s
""" %(self.job_id, self.resource_type, self.n_resource, 
self.run_time, self.job_name, self.email, self.command_line)
        return content
    
    def batch(self):
        self.batch_file= tempfile.NamedTemporaryFile(delete= False, suffix= ".sh")
        self.batch_file.write(self.content)
        self.batch_file.close()
        #os.unlink(self.batch_file.name)
        
        #batch_line= "sbatch %s" %self.batch_file.name
        #batch_line= "bash %s \&" %self.batch_file.name
        #p= subprocess.Popen(batch_line, shell= True, 
        #        stdout= subprocess.PIPE, stderr= subprocess.PIPE)

        #out, err= p.communicate()
        

        #print out 
        #print
        #print err

        return self.content
