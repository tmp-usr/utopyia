import os

#server="""

#local= """

### reference
####### TODO: Important: Create symbolic links to the reference files and 
####### refet to the symbolic links rather than the original files TODO

s_ref_root = "~/projects/colon_cancer/reference"


s_ref_genome_dir= os.path.join(s_ref_root, "genomeDir")
s_ref_fasta_file=  os.path.join(s_ref_root, "GRCh38.d1.vd1.fa")
s_ref_gtf_file= os.path.join(s_ref_root, "gencode.v22.annotation.gtf")


#### tmp
tmp_root_dir= os.environ["SNIC_TMP"]



### alignment 
                     
            
            
            
            
            

output_base_dir= "/home/adilm/projects/colon_cancer/outputs" 

local= """
project_base="/Users/kemal/Desktop/postdoc/projects/" 

ref_root_dir= os.path.join(project_base, "reference")
ref_genome_dir= os.path.join(project_base, "reference", "genomeDir")
ref_gtf_file= os.path.join(project_base, "reference", "genome.gtf")
ref_fasta_file= os.path.join(project_base, "reference", "genome.fa")

tmp_root_dir= os.path.join(project_base, "mock/tmp")
output_base_dir= os.path.join(project_base, "mock/output")

"""


