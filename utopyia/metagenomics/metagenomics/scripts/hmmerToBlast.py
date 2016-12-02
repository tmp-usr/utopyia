from collections import namedtuple
import csv

def hmmerToBlast(domtblout, blastout):
    with open('b2h.map') as b2hmap:
        fields=b2hmap.next().rstrip()
        Blast2Hmmer= namedtuple('Blast2Hmmer',fields.split(':'))
        #for line in b2hmap:
        mapper= map(Blast2Hmmer._make, csv.reader(b2hmap, delimiter=':'))
    with open(domtblout) as hmmerOut, open(blastout,'w') as bOut:
        for line in hmmerOut:
            bLine= ['-']*12
            if not line.startswith('#'):
                cols= line.rstrip().lstrip().split()
                for i in range(12):
                    try:    
                        eq= int(mapper[i].cHmmer)-1
                        bLine[i]= cols[int(eq)]
                    except:
                        continue
                bOut.write('\t'.join(bLine)+'\n')

