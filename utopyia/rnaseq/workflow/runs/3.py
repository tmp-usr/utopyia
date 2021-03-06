import glob
import os
import sys
from collections import OrderedDict

sys.path.append("../../")

from project.project import Project
from fastq.merger import FastQContainerMerger
from fastq.splitter import FastQContainerSplitter


#3. merge ==> split ==> align (compressed|decompressed) ==> generate_counts

project_name= "mock"
project_dir= "/Users/kemal/Desktop/postdoc/projects/mock_colon_cancer/raw_data"
replication_level= "lane"


p= Project(project_name, project_dir, replication_level= replication_level)
p.populate_fastq_containers()

rep = p.all_fastq_containers.values()[0]
fastq_container_name= p.all_fastq_containers.keys()[0]


fcm= FastQContainerMerger(rep, "./merge_dir")

(merged_1, merged_2)= fcm.merge_container()


update the project containers. get the new container from the project object and feed into the splitter

get the newly built split fastq files as they are generated.

print merged_1, merged_2      

Aligner()




