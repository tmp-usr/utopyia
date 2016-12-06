

class Aligner(object):
    """
        Current alignment tool is STAR. Other option is kallisto.
    
    usage:
        Aligner(fastq_pair, genome_dir1="", genome_dir2="", genome_fasta_path="", 
                sjdb_file_chr_start_end="", sam_out="", gtf_out="", 
                count_out= "")

    """
    def __init__(self, fastq_pair, *args, **kwargs):
        self.output_prefix= "star_sorted_"
        self.fastq_pair= fastq_pair
        self.init_attr(**kwargs)
        


    def init_attr(self, **kwargs):
        if "genome_dir1" in kwargs:
            self.genome_dir1= kwargs["genome_dir1"] 

        if "genome_dir2" in kwargs:
            self.genome_dir2= kwargs["genome_dir2"]
 
        if "genome_fasta_path" in kwargs:
            self.genome_fasta_path= kwargs["genome_fasta_path"]

        if "sjdb_file_chr_start_end" in kwargs:
            self.sjdb_file_chr_start_end= kwargs["sjdb_file_chr_start_end"]

        if "sam_out" in kwargs:
            self.sam_out = kwargs["sam_out"]

        if "gtf_out" in kwargs:
            self.gtf_out= kwargs["gtf_out"]

        if "count_out" in kwargs:
            self.count_out= kwargs["count_out"]



    def align_fastq_pair(self, aligner= "star"):
        if aligner == "star":
            self.star_step_1()
            self.star_step_2()
            self.star_step_3()


    def star_step_1(self):
        command_line= """STAR --genomeDir %s --readFilesIn %s %s 
        --runThreadN 16 --outFilterMultimapScoreRange 1 
        --readFilesCommand gunzip -c
        --outFilterMultimapNmax 20 --outFilterMismatchNmax 10 
        --alignIntronMax 500000 --alignMatesGapMax 1000000 
        --sjdbScore 2 --alignSJDBoverhangMin 1 --genomeLoad NoSharedMemory 
        --outFilterMatchNminOverLread 0.33 --outFilterScoreMinOverLread 0.33 
        --sjdbOverhang 100 --outSAMstrandField intronMotif 
        --outSAMtype None --outSAMmode None """ % (
                self.genome_dir1, self.fastq_pair[0], self.fastq_pair[1])


    def star_step_2(self):
         command_line= """STAR --runMode genomeGenerate --genomeDir %s 
        --genomeFastaFiles %s --sjdbOverhang 100 --sjdbFileChrStartEnd %s 
        --runThreadN 16""" % (self.genome_dir2, self.genome_fasta_path, 
                self.sjdb_file_chr_start_end )
   

    def star_step_3(self):
        command_line= """STAR --genomeDir %s --readFilesIn %s %s 
        --runThreadN 16 --outFilterMultimapScoreRange 1 
        --readFilesCommand gunzip -c
        --outFilterMultimapNmax 20 --outFilterMismatchNmax 10 
        --alignIntronMax 500000 --alignMatesGapMax 1000000 
        --sjdbScore 2 --alignSJDBoverhangMin 1 
        --genomeLoad NoSharedMemory --limitBAMsortRAM 70000000000 
        --outFilterMatchNminOverLread 0.33 --outFilterScoreMinOverLread 0.33 
        --sjdbOverhang 100 --outSAMstrandField intronMotif 
        --outSAMattributes NH HI NM MD AS XS --outSAMunmapped Within 
        --outSAMtype BAM SortedByCoordinate --outSAMheaderHD @HD VN:1.4
        --outFileNamePrefix %s """ %(self.genome_dir2, self.fastq_pair[0],
                self.fastq_pair[1], self.output_prefix)
 


