#!/bin/bash

if [ $# -lt 2 ];then
	echo "[usage] $0 input.file outprefix"
	exit 1;
fi


inFile=$1
outPrefix=$2

outGeneFile=$outPrefix.genes.txt
outIsoformFile=$outPrefix.isoforms.txt

geneAnnots=$outPrefix.gene.annot.txt
isoformAnnots=$outPrefix.isoform.annot.txt
tpmValues=$outPrefix.tpm.values.txt
metaFile=$outPrefix.meta.txt


if [ ! -f $inFile ];then
	echo "input file is not existing"
	exit 1;
fi

#extracting annotations 
cat $inFile | sed "1d" | awk 'BEGIN{FS="|"}{print $1}' > $isoformAnnots
cat $inFile | sed "1d" | awk 'BEGIN{FS="|"}{print $2}' > $geneAnnots
cat $inFile | sed "1d" | awk 'BEGIN{FS="\t"}{print $5}' > $tpmValues

paste $isoformAnnots $tpmValues > $outIsoformFile
paste $geneAnnots $isoformAnnots $tpmValues > $metaFile
cat $metaFile | awk '{ if($1 in geneTpm) geneTpm[$1] = geneTpm[$1]+ $3; else geneTpm[$1]=$3;}END{for (gene in geneTpm) printf "%s\t%.6f\n", gene, geneTpm[gene]}'  > $outGeneFile


echo `cat $outIsoformFile | wc -l`
echo `cat $outGeneFile | wc -l`

rm $metaFile
rm $geneAnnots
rm $isoformAnnots
rm $tpmValues

