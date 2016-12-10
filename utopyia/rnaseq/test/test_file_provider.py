import sys
import os

sys.path.append(os.path.join(os.path.abspath("."),'..'))

from config.file_provider import RNASeqOutputProvider


output_root_dir= "/Users/kemal/Desktop/postdoc/projects/mock/outputs"

rp= RNASeqOutputProvider(output_root_dir= output_root_dir)
print rp.tmp_provider.merge_split_dir
print rp.get_alignment_provider("hamza").sam_file
print rp.get_alignment_provider("hamza").count_file




