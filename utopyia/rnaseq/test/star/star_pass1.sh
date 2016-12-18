module load bioinfo-tools
module load star/2.4.2a
module load samtools/1.1


read1=/home/adilm/projects/mock/tmp/merge_split_dir/sample_1/split/reads_1_sp/reads_1_1.fastq
read2=/home/adilm/projects/mock/tmp/merge_split_dir/sample_1/split/reads_2_sp/reads_2_1.fastq
outTmpDir=./myTmpDir
outFileNamePrefix=./myOutputs/mySample

genomeDir=/home/adilm/projects/reference_genomes/human/genomeDir


STAR --genomeDir $genomeDir --readFilesIn $read1 $read2 --runThreadN 16 --outFilterMultimapScoreRange 1 --outFilterMultimapNmax 20 --outFilterMismatchNmax 10 --alignIntronMax 500000 --alignMatesGapMax 1000000 --sjdbScore 2 --alignSJDBoverhangMin 1 --genomeLoad NoSharedMemory --outFilterMatchNminOverLread 0.33 --outFilterScoreMinOverLread 0.33 --sjdbOverhang 100 --outSAMstrandField intronMotif --outSAMtype None --outSAMmode None --outTmpDir $outTmpDir --outFileNamePrefix $outFileNamePrefix



        
