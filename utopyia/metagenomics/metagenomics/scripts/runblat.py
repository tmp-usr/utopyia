import luigi
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
import os 
from Bio import SeqIO

class RunBlat(DependencyMetaTask):
    """
    as far as I could find mothur does not allow changing output file names. this was annoying. use any of the other command line trimming tools. FastQPolish is preferred here.

    """
    
    fastaFile= luigi.Parameter()
    #pathToBlat= luigi.Parameter()
    blatDB=luigi.Parameter()
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
    
    def output(self):
        db=self.get_input('db')
        return { 'blat': 
                    luigi.LocalTarget(
                       'alignment/blat/' + os.path.basename(self.get_input('fastaFile').path).replace('.faa','.%s.blat' %db )),
                  #'discard': 
                  #  luigi.LocalTarget(
                  # 'discard/' +  os.path.basename(self.get_input('fastqFile').path).replace('.fastq','.discard.fastq'))
                }
        #print 'finished'
        #    return luigi.LocalTarget("trimmed/%s.fasta" %self.sample)
    
    
    def runBlat(self):
        #mothurCmd = "\"#trim.seqs(fasta=%s, qfile=%s, qwindowaverage=%s, minlength=%s)\"" %(fastaFile, qualFile, qThreshold, minSeqLen)
        #mothurLoc= "/Users/kemal/mothur/mothur"
        #return [ mothurLoc , mothurCmd ]  
        fBlat= self.output()['blat'].path
        
        if not os.path.exists(os.path.dirname(fBlat)):
            os.makedirs(os.path.dirname(fBlat))
        
        
        #fDiscard= self.output()['discard'].path
        
        #if not os.path.exists(os.path.dirname(fDiscard)):
        #    os.makedirs(os.path.dirname(fDiscard))

        #with open(fTrim,'w') as trim:
        #    SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
        fastaFile= self.get_input('fastaFile').path
        blatDB= self.get_input('blatDB')
        #blastn -query a -out a.blast -remote -db nr -outfmt 6 -evalue 1e-5
        #cmd= ["fastqp.py", "-i", self.fastqFile, "-o" , fTrim,"-d",fDiscard, "-q", self.qThreshold, "-x", str(minSeqLen)]
        #cmds=['/usr/local/bin/blat','-prot','-minMatch=3',',tileSize=3','-dots=100','-out=blast8',db,query,newfile]
        cmd= ['blat', blatDB, fastaFile, fBlat, '-prot','-minMatch=3','tileSize=3','-dots=100','-out=blast8']
        # "-perc_identity", "60":  not found in blastp
        cmd= ' '.join(cmd) 
        print cmd
        run_cmd(cmd)
    
    def run(self):
        print '==== Running Blat ===='
        self.runBlat() 


