#!/bin/bash -l

#SBATCH -A b2016253  
#SBATCH -p core
#SBATCH -n 16
#SBATCH -t 0:30:00
#SBATCH -J kallisto.quant.new.GRCh38.kemal
#SBATCH --mail-type=ALL

#### SNIC2016-1-184

####SBATCH --mail-user kemalsanli1@gmail.com
echo "this script will use 16 cores and 30 mins wall time (maximum execution time)"

if [ $# -lt 4 ];then
	echo '[usage] $0 pair1_sample pair2_sample sample_number output_dir'
	exit 1;
fi

indFile=/proj/b2016253/genome/hg19.kallisto.GRCh38.index

pair1=$1
pair2=$2
num=$3
outDir=$4


#if [ ! -d $outDir ];then
#	mkdir -p $outDir
#fi

#loading kallisto library
#module load kallisto/0.43.0

#preprocessing raw file by kallisto
echo "kallisto preprocessing"
kallisto quant -i $indFile -o $outDir -t 16 --bootstrap-samples=100 $pair1 $pair2
echo "preprocessed"

#parsing kallisto output and saving parsed result into outDir
echo "parsing kallisto output" 
bash /home/adilm/repos/rnaseq/rnaseq/kallisto.isoform.to.gene.sh $outDir/abundance.tsv  $outDir/rnaseq.$num

#cleaning data
echo "Removing the decompressed fastq pair."
rm $pair1 $pair2 
rm $outDir/*.out

echo "finished"


