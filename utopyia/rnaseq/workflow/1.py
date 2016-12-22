import glob
import os
import sys
from collections import OrderedDict

sys.path.append("../")

from merge import MergeContainer
from split import SplitContainer
from populate_project import PopulateProject
from align import Align

#3. split ==> align (compressed|decompressed) ==> generate_counts


### task1 : walk through the project dirs and populate samples
p = PopulateProject()
rep = p.all_fastq_containers.values()[0]
fastq_container_name= p.all_fastq_containers.keys()[0]

### task2 : split the fastq files in each container
fcs= SplitContainer(rep)
fastq_pair_generator= fcs.run()



import time
from pprint import pprint as pp


for pair in fastq_pair_generator:
    Align(rep, pair[0], pair[1], p.learner).run()
    print pair
    time.sleep(2)
    
#for result in fastq_pair_generator:
#    for i, pair in enumerate(result, 1):
#        print pp(pair))
#        time.sleep(2)
        #Aligner!!!


#### consider using the command line tool fswatch with the below 
# listed options until the logger is fixed. The task module with 
# the loggers set will be more powerful! UNTIL THEN!!!
# fswatch --recursive -t -u .

