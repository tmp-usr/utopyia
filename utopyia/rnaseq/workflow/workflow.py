import glob
import os
import sys
from collections import OrderedDict

sys.path.append("../")

import functools
from merge import MergeContainer
from split import SplitContainer
from populate_project import PopulateProject
from align import Align
from count import Count

from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool


import pdb

#3. split ==> align (compressed|decompressed) ==> generate_counts

class Workflow1(object):
    def __init__(self, project):
        self.project= project
        #self.aln_output_dirs= {}

    def run_split_and_alignment(self, fastq_container, project): #, aln_output_dirs):
        ### task2 : split the fastq files in each container
        fcs= SplitContainer(fastq_container)
        fastq_pair_generator= fcs.run()

        for i, pair in enumerate(fastq_pair_generator,1):
            aln= Align(fastq_container, pair[0], pair[1], project.learner)
            #aln_name= aln.name
            #aln_output_dir= aln.io_provider.output_provider.output_dir.path 
            #self.aln_output_dirs[aln_name] = aln_output_dir
            aln.run() 

    def run_parallel(self, project): #, aln_output_dirs):
        fastq_containers= project.all_fastq_containers.values()
        

        #p= Pool(processes=cpu_count)
        #p.map(functools.partial(self.run_split_and_alignment, project= project), fastq_containers)
    
        for fastq_container in fastq_containers:
            self.run_split_and_alignment(fastq_container, project=project)
        

    def generate_output(self):
        cnt=  Count(level = "gene", method= "kallisto")
        alignment_outputs= cnt.set_alignment_outputs()
        return cnt.count(alignment_outputs)    




### task1 : walk through the project dirs and populate samples
project1 = PopulateProject()
#fastq_container_name= p.all_fastq_containers.keys()[1]

workflow1= Workflow1(project1)
workflow1.run_parallel(project1)
print workflow1.generate_output()


#for result in fastq_pair_generator:
#    for i, pair in enumerate(result, 1):
#        print pp(pair))
#        time.sleep(2)
        #Aligner!!!


#### consider using the command line tool fswatch with the below 
# listed options until the logger is fixed. The task module with 
# the loggers set will be more powerful! UNTIL THEN!!!
# fswatch --recursive -t -u .

