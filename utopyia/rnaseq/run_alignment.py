
from dependencymixin import DependencyMetaTask

genome_dir1= "/proj/b2016253/nobackup/genomeDir"
genome_dir2= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/genomeDir"
genome_dir3= genome_dir2
genome_fasta_files= "/proj/b2016253/nobackup/GRCh38.d1.vd1.fa"


sjdb_file_chr_start_end= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/SJ.out.tab"
sam_out= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/Aligned.sortedByCoord.out.bam"
gtf_output= "/proj/b2016253/nobackup/gencode.v22.annotation.gtf"
count_output= "/proj/b2016253/nobackup/1_130213_AH07R5ADXX_P282_102B_index25/adrenal_4a_P282_102.count"


class RunStarAlignment(DependencyMetaTask):
    
    genome_dir1= luigi.Parameter()
    genome_dir2= luigi.Parameter()
    genome_fasta_path= luigi.Parameter()
    sjdb_file_chr_start_end= luigi.Parameter()
    
    sam_out= luigi.Parameter()
    gtf_out= luigi.Parameter()
    count_out= luigi.Parameter()

    def output(self):    
        pass


    def step_1(self):
        command_line= """STAR --genomeDir %s --readFilesIn %s %s 
        --runThreadN 16 --outFilterMultimapScoreRange 1 
        --outFilterMultimapNmax 20 --outFilterMismatchNmax 10 
        --alignIntronMax 500000 --alignMatesGapMax 1000000 
        --sjdbScore 2 --alignSJDBoverhangMin 1 --genomeLoad NoSharedMemory 
        --outFilterMatchNminOverLread 0.33 --outFilterScoreMinOverLread 0.33 
        --sjdbOverhang 100 --outSAMstrandField intronMotif 
        --outSAMtype None --outSAMmode None """ % (genome_dir1, fastq_read1, fastq_read2)

    def step_2(self):
        command_line= """STAR --runMode genomeGenerate --genomeDir %s 
        --genomeFastaFiles %s --sjdbOverhang 100 --sjdbFileChrStartEnd %s 
        --runThreadN 16""" % (genome_dir2, genome_fasta_path, sjdb_file_chr_start_end )

    def step_3(self):
        command_line= """STAR --genomeDir %s --readFilesIn %s %s 
        --runThreadN 16 --outFilterMultimapScoreRange 1 
        --outFilterMultimapNmax 20 --outFilterMismatchNmax 10 
        --alignIntronMax 500000 --alignMatesGapMax 1000000 
        --sjdbScore 2 --alignSJDBoverhangMin 1 
        --genomeLoad NoSharedMemory --limitBAMsortRAM 70000000000 
        --outFilterMatchNminOverLread 0.33 --outFilterScoreMinOverLread 0.33 
        --sjdbOverhang 100 --outSAMstrandField intronMotif 
        --outSAMattributes NH HI NM MD AS XS --outSAMunmapped Within 
        --outSAMtype BAM SortedByCoordinate --outSAMheaderHD @HD VN:1.4
        --outFileNamePrefix %s """ %(genome_dir3, fastq_read1, fastq_read2, output_prefix)
        

    def run_alignment(self):
        self.step1()
        self.step2()
        self.step3()


    def run(self):
        self.run_alignment()
