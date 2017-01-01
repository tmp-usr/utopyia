#!/bin/bash -l

#SBATCH -A snic2016-1-184
#SBATCH -p core
#SBATCH -n 8
#SBATCH -t 10:00:00
#SBATCH -J rnaseq_pipeline
#SBATCH --mail-user kemal.sanli@scilifelab.se
#SBATCH --mail-type=ALL

python workflow.py

