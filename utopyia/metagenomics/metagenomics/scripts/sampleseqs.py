from Bio import SeqIO
from random import randint
from dependencymixin import DependencyMetaTask
import os
import luigi


class SampleSeqs(DependencyMetaTask):
    
    nSequence= luigi.Parameter()
    trimmedFile= luigi.Parameter() 


    def output(self):
        return { 'fastq': 
                    luigi.LocalTarget(
                       'random/'+ os.path.basename(self.get_input('trimmedFile').path).replace('.fastq','.%s.fastq' % self.get_input('nSequence'))),
                
                
                'fasta': 
                    luigi.LocalTarget(
                       'random/'+ os.path.basename(self.get_input('trimmedFile').path).replace('.fastq','.%s.fasta' % self.get_input('nSequence'))),
                
                'qual': 
                    luigi.LocalTarget(
                       'random/'+ os.path.basename(self.get_input('trimmedFile').path).replace('.fastq','.%s.qual' % self.get_input('nSequence'))),


                    }    

    
    def extractIds(self):
        self.trimmedFile= self.get_input('trimmedFile').path
        handle= open(self.trimmedFile)
        records= SeqIO.parse(handle, "fastq")
        return [rec.id for rec in records]
    
    def randomSampleSequences(self):
        ids= self.extractIds()
        nSequence= self.get_input('nSequence')
        nSequence=int(nSequence)
        rndIds=[ids[randint(0,len(ids))] for i in range(nSequence)]
        return rndIds

    def run(self):
        print "=== Randomly Sampling %s Sequences ===" % self.get_input('nSequence')
        ids= self.randomSampleSequences()
        #handle= open(self.trimmedFile)
        rec_dict= SeqIO.index(self.trimmedFile, "fastq")
        seqs= [rec_dict.get_raw(i) for i in ids]
        
        fFastq= self.output()['fastq'].path
        fFasta= self.output()['fasta'].path
        fQual= self.output()['qual'].path
        


        if not os.path.exists(os.path.dirname(fFastq)):
            os.makedirs(os.path.dirname(fFastq))
        
        with open(fFastq,'w') as fqFile:
            fqFile.write(''.join(seqs))
        records= list(SeqIO.parse(open(fFastq,'rU'), 'fastq'))
        SeqIO.write(records, fFasta, 'fasta')
        SeqIO.write(records, fQual, 'qual') 


