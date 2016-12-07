import os
import shutil

from aligner import Aligner
from project.project import Project

### TODO: define s_no


p= Project("colon_cancer", "/proj/b2014274/INBOX/F.Ponten_16_01", replication_level = "lane")




trash_0="""
#### disk space for large temporary files
tmp_dir= os.environ["SNIC_TMP"]
output_base= tmp_dir
genome_dir1= "/proj/b2016253/nobackup/genomeDir"
genome_dir2= os.path.join(tmp_dir, "genomeDir_%s" %(s_no))

if not os.path.exists(genome_dir2):
    os.mkdir(genome_dir2)

genome_dir3= genome_dir2
genome_fasta_path= "/proj/b2016253/nobackup/GRCh38.d1.vd1.fa"

output_dir= "/home/adilm/repos/utopyia/utopyia/rnaseq/output/%s" % s_no

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


tmp_output_dir_1= os.path.join(tmp_dir, "tmp_1/")
tmp_output_dir_2= os.path.join(tmp_dir, "tmp_2/")
#tmp_output_dir_2= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_output/tmp_2/"

if os.path.exists(tmp_output_dir_1):
    shutil.rmtree(tmp_output_dir_1)

if os.path.exists(tmp_output_dir_2):
    shutil.rmtree(tmp_output_dir_2)



sj_out= os.path.join(output_dir, "SJ.out.tab")
sam_output= os.path.join(output_dir, "Aligned.sortedByCoord.out.bam")
gtf_file= "/proj/b2016253/nobackup/gencode.v22.annotation.gtf"
count_output= os.path.join(output_dir, "count.txt")

"""


trash="""
test_data_base= "/home/adilm/repos/utopyia/utopyia/rnaseq/test_data/"

fastq_1= os.path.join(test_data_base, "reads_1.fastq.gz")
fastq_2= os.path.join(test_data_base, "reads_2.fastq.gz")

fastq_pair= (fastq_1, fastq_2)

aln= Aligner(fastq_pair=fastq_pair, genome_dir1=genome_dir1, genome_dir2=genome_dir2, 
        genome_fasta_path=genome_fasta_path, sj_out=sj_out, 
        sam_out= sam_output, gtf_file=gtf_file, count_out= count_output, 
        tmp_output_dir_1= tmp_output_dir_1, tmp_output_dir_2= tmp_output_dir_2,
        output_dir= output_dir)

aln.align_fastq_pair()
"""



