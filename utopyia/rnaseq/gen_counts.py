from dependencymixin import DependencyMetaTas

sam_out= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/Aligned.sortedByCoord.out.bam"
gtf_out= "/proj/b2016253/nobackup/gencode.v22.annotation.gtf"
count_out= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/adrenal_4a_P282_102.count"


class GenCounts(DependencyMetaTask):
        
    sam_out = luigi.Parameter()
    gtf_out = luigi.Parameter()
    count_out= luigi.Parameter()

    def output(self):
       pass 


    def gen_counts(self):
        command_line= """
        module load samtools/1.1
        samtools view -F 4 %s | htseq-count -m intersection-nonempty -i gene_id -r pos -s no -t exon - %s > %s
        """ %(sam_out, gtf_out, count_out)



    def run(self):
        self.gen_counts()



