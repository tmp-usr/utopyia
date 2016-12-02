import luigi
from convertsff import ConvertSff
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
import os 
from Bio import SeqIO


class TrimSeqs(DependencyMetaTask):
    """
    as far as I could find mothur does not allow changing output file names. this was annoying. use any of the other command line trimming tools. FastQPolish is preferred here.

    """
    
    qThreshold= luigi.Parameter()
    fastqFile= luigi.Parameter()
    #qualFile= luigi.Parameter()
    
    #sample
    ### here we should be able play with the parameters such as sliding window size, quality threshold and minimum sequence length
    #def requires(self):
    #    sffconversion= ConvertSff(3

    #    return ConvertSff(self.sample)
    
    def output(self):
        qThreshold=self.get_input('qThreshold')
        fastqFile= self.get_input('fastqFile')
        return { 'fastq': 
                    luigi.LocalTarget(
                       'trim/fastq/'+ os.path.basename(fastqFile.path).replace('.fastq','.trim.%s.fastq' %qThreshold)),

                 'fasta': 
                    luigi.LocalTarget(
                       'trim/fasta/'+ os.path.basename(fastqFile.path).replace('.fastq','.trim.%s.fasta' %qThreshold)),
 #'discard': 'fastq': 
                  'qual': luigi.LocalTarget(
                       'trim/qual/'+ os.path.basename(fastqFile.path).replace('.fastq','.trim.%s.qual' %qThreshold)),

                  #  luigi.LocalTarget(
                  # 'discard/' +  os.path.basename(self.get_input('fastqFile').path).replace('.fastq','.discard.fastq'))
                }
        #print 'finished'
        #    return luigi.LocalTarget("trimmed/%s.fasta" %self.sample)
    
    
    def trimSeqs(self, windowSize= 50, minSeqLen=100):
        #mothurCmd = "\"#trim.seqs(fasta=%s, qfile=%s, qwindowaverage=%s, minlength=%s)\"" %(fastaFile, qualFile, qThreshold, minSeqLen)
        #mothurLoc= "/Users/kemal/mothur/mothur"
        #return [ mothurLoc , mothurCmd ]  
        fFastq= self.output()['fastq'].path
        fFasta= self.output()['fasta'].path
        fQual= self.output()['qual'].path
        
        if not os.path.exists(os.path.dirname(fFastq)):
            os.makedirs(os.path.dirname(fFastq))
        
        if not os.path.exists(os.path.dirname(fFasta)):
            os.makedirs(os.path.dirname(fFasta))

        if not os.path.exists(os.path.dirname(fQual)):
            os.makedirs(os.path.dirname(fQual))


        #with open(fTrim,'w') as trim:
        #    SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
        self.fastqFile= self.get_input('fastqFile').path
        self.qThreshold= self.get_input('qThreshold')
                
        #cmd= ["fastqp.py", "-i", self.fastqFile, "-o" , fTrim,"-d",fDiscard, "-q", self.qThreshold, "-x", str(minSeqLen)]
        cmd= ["sickle se", '-t','sanger', "-f", self.fastqFile, "-o" , fFastq, "-q", self.qThreshold, "-l", str(minSeqLen), '-x']
        cmd= ' '.join(cmd) 
        
        run_cmd(cmd)
        records = list(SeqIO.parse(fFastq, "fastq"))
        SeqIO.write(records, fFasta, "fasta")
        SeqIO.write(records, fQual, "qual")
            

    def run(self):
        print '==== trimming sequences ===='
        self.trimSeqs() 

