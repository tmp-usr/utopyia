#!/bin/bash
#SBATCH -A b2016253  
#SBATCH -p core
#SBATCH -n 8
#SBATCH -t 0:30:00
#SBATCH -J bz2.decompression.kemal
#SBATCH --mail-type=ALL

# SNIC2016-1-184


if [ $# -lt 1 ];then
	echo "[usage] $0 file.bz2"
	exit 1
fi

compressed_file=$1
decompressed_file=$2

zcat -d $compressed_file > $decompressed_file

