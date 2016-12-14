def star_pass_1(genome_dir1, fastq_pair, tmp_output_dir_1, output_dir):
    command_line= """
#module load bioinfo-tools star/2.4.2a
STAR \
--readFilesIn %s %s \
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
--outSAMtype None \
--outFileNamePrefix %s
""" % (fastq_pair.reads_1, fastq_pair.reads_2, genome_dir1, tmp_output_dir_1, output_dir)
    return command_line

def star_pass_2(genome_dir2, genome_fasta_path, sj_out):
    command_line= """
STAR \
--runMode genomeGenerate \
--genomeDir %s \
--genomeFastaFiles %s \
--sjdbOverhang 100 \
--sjdbFileChrStartEnd %s \
--runThreadN 16
""" % (genome_dir2, genome_fasta_path, sj_out )
    return command_line

def star_pass_3(genome_dir2, fastq_pair, tmp_output_dir_2, output_prefix):
    command_line= """
STAR \
--genomeDir %s \
--readFilesIn %s %s \
--runThreadN 16 \
--outFilterMultimapScoreRange 1 \
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
""" %(genome_dir2, fastq_pair.reads_1, fastq_pair.reads_2, tmp_output_dir_2, output_prefix)
    return command_line


def generate_counts(bam_out, gtf_file, count_out):
    command_line= """
#module load samtools/1.1
samtools view -F 4 %s | htseq-count -m intersection-nonempty -i gene_id -r pos -s no -t exon - %s > %s 
""" % (bam_out, gtf_file, count_out)
    return command_line
