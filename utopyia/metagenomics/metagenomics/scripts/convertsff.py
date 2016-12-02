import luigi
from Bio import SeqIO
from dependencymixin import DependencyMetaTask
import os

class ConvertSff(DependencyMetaTask):
#class ConvertSff(luigi.Task):

    sample = luigi.Parameter()

    def output(self):
        
        sample= os.path.basename(self.get_input('sample')).replace('.sff','') 
        return { 'fasta': 
                    luigi.LocalTarget(
                       'raw/fasta/'+ sample+'.fasta'),
                  'qual': 
                    luigi.LocalTarget(
                      'raw/qual/' + sample+'.qual'),
                  'fastq': 
                    luigi.LocalTarget(
                   'raw/fastq/' +  sample+'.fastq')
                }

    def convertSff(self):
        """
            converts the sff file to fasta, qual and fastq files
        """
        sffFile= self.get_input('sample')

        fFasta=  self.output()['fasta'].path
        fQual=  self.output()['qual'].path 
        fFastq= self.output()['fastq'].path  
        
        if not os.path.exists(os.path.dirname(fFasta)):
            os.makedirs(os.path.dirname(fFasta))
        
        with open(fFasta,'w') as fasta:
            SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
        
        if not os.path.exists(os.path.dirname(fQual)):
            os.makedirs(os.path.dirname(fQual))
        
        with open(fQual,'w') as qual:
            SeqIO.convert(sffFile, "sff-trim", qual, "qual")

        if not os.path.exists(os.path.dirname(fFastq)):
            os.makedirs(os.path.dirname(fFastq))
        
        with open(fFastq,'w') as fastq:
            SeqIO.convert(sffFile, "sff-trim", fastq, "fastq")


    def run(self):
        print "=== Converting Sff ==="
        self.convertSff()


