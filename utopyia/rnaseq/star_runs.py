def star_pass_1(genome_dir1, fastq_pair, tmp_output_dir_1):
    command_line= """
module load bioinfo-tools star/2.4.2a
STAR \
--readFilesIn %s %s \
--readFilesCommand gunzip -c \
--genomeDir %s \
--outTmpDir %s \
--runThreadN 16 \
--outFilterMultimapScoreRange 1 \
--outFilterMultimapNmax 20 \
--outFilterMismatchNmax 10 \
--alignIntronMax 500000 \
--alignMatesGapMax 1000000 \
--sjdbScore 2 \
--alignSJDBoverhangMin 1 \
--genomeLoad NoSharedMemory \
--outFilterMatchNminOverLread 0.33 \
--outFilterScoreMinOverLread 0.33 \
--sjdbOverhang 100 \
--outSAMstrandField intronMotif \
--outSAMtype None
--outSAMmode None
""" % (fastq_pair[0], fastq_pair[1], genome_dir1, tmp_output_dir_1)
    return command_line

def star_pass_2(genome_dir2, genome_fasta_path, sjdb_file_chr_start_end):
    command_line= """
module load bioinfo-tools star/2.4.2a  
STAR \
--runMode genomeGenerate \
--genomeDir %s \
--genomeFastaFiles %s \
--sjdbOverhang 100 \
--sjdbFileChrStartEnd %s \
--runThreadN 16
""" % (genome_dir2, genome_fasta_path, sjdb_file_chr_start_end )
    return command_line

def star_pass_3(genome_dir2, fastq_pair, tmp_output_dir_2, output_prefix):
    command_line= """
module load bioinfo-tools star/2.4.2a     
STAR \
--genomeDir %s \
--readFilesIn %s %s \
--runThreadN 16 \
--outFilterMultimapScoreRange 1 \
--readFilesCommand gunzip -c \
--outTmpDir %s \
--outFilterMultimapNmax 20 \
--outFilterMismatchNmax 10 \
--alignIntronMax 500000 \
--alignMatesGapMax 1000000 \
--sjdbScore 2 \
--alignSJDBoverhangMin 1 \
--genomeLoad NoSharedMemory \
--limitBAMsortRAM 70000000000 \
--outFilterMatchNminOverLread 0.33 \
--outFilterScoreMinOverLread 0.33 \
--sjdbOverhang 100 \
--outSAMstrandField intronMotif \
--outSAMattributes NH HI NM MD AS XS \
--outSAMunmapped Within \
--outSAMtype BAM SortedByCoordinate \
--outSAMheaderHD @HD VN:1.4 \
--outFileNamePrefix %s
""" %(genome_dir2, fastq_pair[0], fastq_pair[1], tmp_output_dir_2, output_prefix)
    return command_line
