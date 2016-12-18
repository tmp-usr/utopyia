import os



compression_method= "bzip"

#local
project_root_dir= "/Users/kemal/Desktop/postdoc/projects/mock_low_carb"

#server
#project_root_dir= "/home/adilm/projects/mock_low_carb/"



##### reference
####### TODO: Important: Create symbolic links to the reference files and 
####### refet to the symbolic links rather than the original files TODO



#local
#s_ref_root = os.path.join("/Users/kemal/Desktop/postdoc/projects/", "reference_genomes")

#server
#s_ref_root = os.path.join("/home/adilm/projects/colon_cancer", "reference")
s_ref_root = "/Users/kemal/Desktop/postdoc/projects/mock_low_carb/reference/"

k_ref_genome_index= "/proj/b2016253/genome/hg19.kallisto.GRCh38.index"

s_ref_genome_dir= "genomeDir"
s_ref_fasta_file=  "GRCh38.d1.vd1.fa"
s_ref_gtf_file= "gencode.v22.annotation.gtf"
#s_ref_gtf_file= ""


#### tmp
# local 
tmp_root_dir= os.path.join(project_root_dir, "tmp")

# server
#tmp_root_dir=  os.environ["SNIC_TMP"]
#tmp_root_dir= os.path.join(project_root_dir, "tmp") 
