import os


#local
project_root_dir= "/Users/kemal/Desktop/postdoc/projects/mock"

#server
#project_root_dir= "/home/adilm/projects/colon_cancer/"



##### reference
####### TODO: Important: Create symbolic links to the reference files and 
####### refet to the symbolic links rather than the original files TODO

s_ref_root = os.path.join(project_root_dir, "reference")

s_ref_genome_dir= "genomeDir"
s_ref_fasta_file=  "GRCh38.d1.vd1.fa"
s_ref_gtf_file= "gencode.v22.annotation.gtf"


#### tmp
# local 
tmp_root_dir= os.path.join(project_root_dir, "tmp")

# server
#tmp_root_dir= os.path.join(project_root_dir, "tmp") #os.environ["SNIC_TMP"]
