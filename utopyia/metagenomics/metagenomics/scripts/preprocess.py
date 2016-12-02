from Bio import SeqIO








def randomSampleSequences(nSequence):
    for i in [20,25,30]:
        fOut=open('pp.%s.1000.trim.fasta.ids' %i,'w')
        ids = [id.rstrip('\n') for id in open("pp.%s.trim.fasta.ids" %i, "rU").readlines()] 
        for j in range(nSequence):
            index= randint(0,len(ids))
            #print ids[index]
            fOut.write('%s\n' % ids[index])  #first record
            #fOut.write('%s\n' % records[index].seq) 

