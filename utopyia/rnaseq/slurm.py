from cStringIO import StringIO

import pdb

class Slurm(object):
    
    def __init__(self, job_id, resource_type= "core", n_resource = 8, run_time= "00:30:00",
                       job_name= "", email= ""):
        self.job_id= job_id
        self.resource_type= resource_type
        self.n_resource= n_resource
        self.run_time= run_time
        self.job_name= job_name
        self.email= email
    
    
    def __str__(self):
        return self.create_content()

    
    @property
    def content(self):
        content= """
#!/bin/bash -l

#SBATCH -A %s
#SBATCH -p %s
#SBATCH -n %d
#SBATCH -t %s
#SBATCH -J %s
#SBATCH --mail-user %s
#SBATCH --mail-type=ALL

""" %(self.job_id, self.resource_type, self.n_resource, self.run_time, self.job_name, self.email)
        return content
    
    def batch(self):
        self.batch_file= StringIO()
        self.batch_file.write(self.content)
        
        subprocess()



s= Slurm(1)
s.batch()
