import luigi
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
import os 
from Bio import SeqIO
from collections import namedtuple
import csv,glob
from pandas import DataFrame, Series, concat, merge



def extractReadAnnotations(blastOutputFile, e_value_t=1e-5, perc_identity_t=60):
    """
        blast output filtering also takes place here.
    """

    bOut=open(blastOutputFile)    
    SampleFunctions={}
    db='nt'
    SampleFunctions[db]={}
    for line in bOut:
        cols=line.rstrip('\n').split('\t')
        read= cols[0]
        function= cols[1]
        perc= cols[2]
        e_value= cols[10]

       
       ### a confirmatory filtering takes place here 
        try:
            if float(perc) < perc_identity_t:
                continue
        except:
            pass

        if float(e_value) > e_value_t:
            continue


        #print function
        # read identifiers must be extended by '_' (underscore) sign if more than 1 sequence is representing the same read.
        # function should be separated by '|' (bar).
        
        sample=read.split('_')[1]
        read= read.split('_')[0]
       
        if read == '':
            continue

        if sample not in SampleFunctions[db]:
            SampleFunctions[db][sample]={}

        if function not in SampleFunctions[db][sample]:
            SampleFunctions[db][sample][function]=[]
            
        SampleFunctions[db][sample][function].append(read)
    return SampleFunctions

        
  

def printFunctions(SampleFunctions):# write count table here
    db='nt'
    fOut= "%s_counts.tsv" %db
    dfs=[]
    for db, Samples in SampleFunctions.iteritems():
        for sample, Functions in Samples.iteritems():
            sampleData= DataFrame(map(len, Functions.values()), index= Functions.keys(), columns=[sample] )
            dfs.append(sampleData)

        df_all=dfs[0].join(dfs[1:],how='outer').fillna(0)
        df_all.index.name='Function'
        cols= sorted(df_all.columns.tolist())
        df_all= df_all[cols]
        df_all.to_csv(fOut, sep='\t', float_format="%d")



blastOutputFile= "pp_gi_only_trimmed.blast"
SF= extractReadAnnotations(blastOutputFile)
printFunctions(SF)

