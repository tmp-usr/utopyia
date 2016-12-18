def star_pass_1(genome_dir1, fastq_pair, tmp_output_dir_1, output_prefix):
    command_line= """
indFile=/proj/b2016253/genome/hg19.kallisto.GRCh38.index

sampleID=1 

pair1=$1
pair2=$2
num=$3
outDir=$4

$num=$sampleID


#loading kallisto library
#module load kallisto/0.43.0

#preprocessing raw file by kallisto
echo "kallisto preprocessing"
kallisto quant -i $indFile -o $outDir -t 16 $pair1 $pair2
echo "preprocessed"
"""
