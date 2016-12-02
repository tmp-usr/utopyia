import sys
import os

hmmer_out=sys.argv[1]
abundance_out=sys.argv[2]


with open(hmmer_out) as f:
    Hits={}
    for line in f:
        if not line.startswith('#'):
            columns=line.rstrip().lstrip().split()
            e_value=float(columns[6])
            if e_value <= 1e-10:
                if columns[4] not in Hits:
                    Hits[columns[4]]=0
                Hits[columns[4]]+=1

with open(abundance_out,'w') as fOut:
    for pfam,count in Hits.iteritems():
        fOut.write(pfam+'\t'+str(count)+'\n')

