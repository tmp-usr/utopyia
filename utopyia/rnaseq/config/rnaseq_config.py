import os

server="""
ref_root_dir= "/proj/b2016253/nobackup"
ref_genome_dir= "/proj/b2016253/nobackup/genomeDir"
ref_fasta_file=  "/proj/b2016253/nobackup/GRCh38.d1.vd1.fa"
ref_gtf_file= "/proj/b2016253/nobackup/gencode.v22.annotation.gtf"

tmp_root_dir= os.environ["SNIC_TMP"]
output_base_dir= "/home/adilm/projects/colon_cancer/outputs" 
"""


#local= """
project_base="/Users/kemal/Desktop/postdoc/projects/" 

ref_root_dir= os.path.join(project_base, "reference")
ref_genome_dir= os.path.join(project_base, "reference", "genomeDir")
ref_gtf_file= os.path.join(project_base, "reference", "genome.gtf")
ref_fasta_file= os.path.join(project_base, "reference", "genome.fa")

tmp_root_dir= os.path.join(project_base, "mock/tmp")
output_base_dir= os.path.join(project_base, "mock/output")

#"""


