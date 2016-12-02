import luigi
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
import os 
from Bio import SeqIO
from collections import namedtuple
import csv

class RunHmmer(DependencyMetaTask):
    """
    as far as I could find mothur does not allow changing output file names. this was annoying. use any of the other command line trimming tools. FastQPolish is preferred here.

    """
    
    fastaFile= luigi.Parameter()
    hmmDB= luigi.Parameter()
    db= luigi.Parameter()
    #### blast params
    #evalue= luigi.Parameter()
    #percent= luigi.Parameter()
    #blastdb=luigi.Parameter()
    
    
    #sample
    ### here we should be able play with the parameters such as sliding window size, quality threshold and minimum sequence length
    #def requires(self):
    #    sffconversion= ConvertSff(3

    #    return ConvertSff(self.sample)
   
    def hmmerToBlast(self, domtblout, blastout):
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
                    if float(bLine[10]) <= 1e-3: 
                    #print bLine
                        bOut.write('\t'.join(bLine)+'\n')


    def output(self):
        fastaFile=self.get_input('fastaFile')
        db=self.get_input('db')
        return { 'hmmer': 
                    luigi.LocalTarget(
                       'alignment/hmmer/' + os.path.basename(fastaFile.path).replace('.faa','.%s.hmmer' %db)),
                 'blast':
                    luigi.LocalTarget(
                       'alignment/hmmer/' + os.path.basename(fastaFile.path).replace('.faa','.%s.blast' %db)),
                  #'discard': 
                  #  luigi.LocalTarget(
                  # 'discard/' +  os.path.basename(self.get_input('fastqFile').path).replace('.fastq','.discard.fastq'))
                }
        #print 'finished'
        #    return luigi.LocalTarget("trimmed/%s.fasta" %self.sample)
    
    
    def runHmmer(self):
        #mothurCmd = "\"#trim.seqs(fasta=%s, qfile=%s, qwindowaverage=%s, minlength=%s)\"" %(fastaFile, qualFile, qThreshold, minSeqLen)
        #mothurLoc= "/Users/kemal/mothur/mothur"
        #return [ mothurLoc , mothurCmd ]  
        fHmmer= self.output()['hmmer'].path
        
        if not os.path.exists(os.path.dirname(fHmmer)):
            os.makedirs(os.path.dirname(fHmmer))
        
        
        #fDiscard= self.output()['discard'].path
        
        #if not os.path.exists(os.path.dirname(fDiscard)):
        #    os.makedirs(os.path.dirname(fDiscard))

        #with open(fTrim,'w') as trim:
        #    SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
        fastaFile= self.get_input('fastaFile').path
        db= self.get_input('hmmDB')
        # hmmsearch --cpu 4 --domtblout out.tsv /home/sanli/dbs/pfam/Pfam-A.hmm input.fasta
        cmd= ['hmmsearch', "-E", "1e-5","--cpu","2", "--domtblout", fHmmer, db, fastaFile ]
        # "-perc_identity", "60":  not found in blastp
        cmd= ' '.join(cmd) 
        print cmd
        run_cmd(cmd)
        
        fBlast= self.output()['blast'].path
        self.hmmerToBlast(fHmmer, fBlast)


    def run(self):
        print '==== Running Hmmer ===='
        self.runHmmer() 
        

