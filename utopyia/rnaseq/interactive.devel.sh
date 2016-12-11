#!/bin/bash

if [ $# -lt 1 ];then
	echo "[usage] interactive.sh core_num_to_use"
	exit 1
fi

coreNum=$1

echo "number of cores will be used is $coreNum"

interactive -A b2016253 -p devcore -n $coreNum -qos=interact -t 01:00:00 -J interactive.devel.reza --mail-user gholamreza.bidkhori@scilifelab.se --mail-type=ALL

interactive -A b2016253 -p core -n 4 -t 00:20:00 -J rnaseq_pipeline --mail-user kemal.sanli@scilifelab.se --mail-type=ALL



