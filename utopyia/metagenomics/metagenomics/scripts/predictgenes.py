import luigi
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
import os 
from Bio import SeqIO

class PredictGenes(DependencyMetaTask):
    """
    as far as I could find mothur does not allow changing output file names. this was annoying. use any of the other command line trimming tools. FastQPolish is preferred here.

    """
    
    fastaFile= luigi.Parameter()
    #fastqFile= luigi.Parameter()
    #qualFile= luigi.Parameter()
    
    #sample
    ### here we should be able play with the parameters such as sliding window size, quality threshold and minimum sequence length
    #def requires(self):
    #    sffconversion= ConvertSff(3

    #    return ConvertSff(self.sample)
    
    def output(self):
        return { 'genes': 
                    luigi.LocalTarget(
                       'genes/'+ os.path.basename(self.get_input('fastaFile').path).replace('.fasta','.fgs.faa')),
                  #'discard': 
                  #  luigi.LocalTarget(
                  # 'discard/' +  os.path.basename(self.get_input('fastqFile').path).replace('.fastq','.discard.fastq'))
                }
        #print 'finished'
        #    return luigi.LocalTarget("trimmed/%s.fasta" %self.sample)
    
    
    def predictGenes(self):
        #mothurCmd = "\"#trim.seqs(fasta=%s, qfile=%s, qwindowaverage=%s, minlength=%s)\"" %(fastaFile, qualFile, qThreshold, minSeqLen)
        #mothurLoc= "/Users/kemal/mothur/mothur"
        #return [ mothurLoc , mothurCmd ]  
        fGenes= self.output()['genes'].path.replace('.faa','')
        
        if not os.path.exists(os.path.dirname(fGenes)):
            os.makedirs(os.path.dirname(fGenes))
        
        
        #fDiscard= self.output()['discard'].path
        
        #if not os.path.exists(os.path.dirname(fDiscard)):
        #    os.makedirs(os.path.dirname(fDiscard))

        #with open(fTrim,'w') as trim:
        #    SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
        fastaFile= self.get_input('fastaFile').path

        #cmd= ["fastqp.py", "-i", self.fastqFile, "-o" , fTrim,"-d",fDiscard, "-q", self.qThreshold, "-x", str(minSeqLen)]
        cmd= ["FGS+", "-s",fastaFile, "-o", fGenes, "-w", "0", "-t","454_10"]
        cmd= ' '.join(cmd) 
        print cmd
        run_cmd(cmd)
    
    def run(self):
        print '==== Predicting Genes ===='
        self.predictGenes() 


