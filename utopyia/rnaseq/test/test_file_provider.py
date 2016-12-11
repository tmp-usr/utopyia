import sys
import os

sys.path.append(os.path.join(os.path.abspath("."),'..'))

from config.file_provider import RNASeqOutputProvider


output_root_dir= "/Users/kemal/Desktop/postdoc/projects/mock/outputs"

op= RNASeqOutputProvider(output_root_dir= output_root_dir)
op.tmp_provider.merge_split_dir
op.get_alignment_provider("hamza").sam_file
op.get_alignment_provider("hamza").count_file


#### reference
s_ref_root = "~/projects/colon_cancer/reference"

s_ref_genome_dir= os.path.join(s_ref_root, "genomeDir")
s_ref_fasta_file=  os.path.join(s_ref_root, "GRCh38.d1.vd1.fa")
s_ref_gtf_file= os.path.join(s_ref_root, "gencode.v22.annotation.gtf")


#### tmp




