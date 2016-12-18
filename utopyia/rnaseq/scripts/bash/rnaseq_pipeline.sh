#!/bin/bash
#SBATCH -A b2016253  
#SBATCH -p core
#SBATCH -n 8
#SBATCH -t 02:00:00
#SBATCH -J rnaseq_pipeline
#SBATCH --mail-type=ALL

# SNIC2016-1-184

python controller.py  >> rnaseq_pipeline.log 2>&1 &
