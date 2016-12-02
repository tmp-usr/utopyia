# builtin
import glob

# third party
import luigi

# library
from convertsff import ConvertSff
from trimseqs import TrimSeqs
from sampleseqs import SampleSeqs
from predictgenes import PredictGenes
from runblast import RunBlast
from runhmmer import RunHmmer
from runblat import RunBlat
from combinealignments import CombineAlignments

##### THE ACTUAL WORKFLOW / DEPENDENCY GRAPH DEFINITION #####

class MyWorkFlow(luigi.Task):
    # We only need to duplicate all parameters 
    # once, which is here in the workflow task
    sample = luigi.Parameter()
    #blatDB= luigi.Parameter()
    #blastCommand= luigi.Parameter()
    #hmmDB= luigi.Parameter()
    qThreshold = luigi.Parameter()
 
    # Here the whole workflow definition resides:
    def requires(self):
        
        convertSff = ConvertSff( 
                sample= self.sample
        )
      
        trimSeqs = TrimSeqs( 
            qThreshold = self.qThreshold,
            #qThreshold =  self.qThreshold,
            # Here below, we connect the output out1 from TaskA
            # to in1_target of TaskB ...
            fastqFile = 
                { 'upstream' : { 'task' : convertSff,
                                 'port' : 'fastq' } },
            # ... and again, out2 of TaskA, to in2_target of
        
        ) 
        
        sampleSeqs= SampleSeqs(
            nSequence = 1000,
            trimmedFile= {
                    'upstream': {'task': trimSeqs,
                                 'port': 'fastq'} ,
                    
                    },
        )

        predictGenes= PredictGenes(
            
            fastaFile= {
                    'upstream': {'task': sampleSeqs,
                                 'port': 'fasta'} ,
                    
                    } ,
            )
       


        #runBlastNr= RunBlast(
        #    blastCommand= self.blastCommand,
        #    fastaFile= {
        #            'upstream': {'task': predictGenes,
        #                         'port': 'genes'} ,
        #            
        #            } ,
        #    )
        

        runBlast= RunBlast(
            blastCommand= "blastp",
            db= "ko",
            fastaFile= {
                    'upstream': {'task': predictGenes,
                                 'port': 'genes'} ,
                    
                    } ,
            )

        runHmmer= RunHmmer(
            hmmDB= "$PFAMDB",
            db='pfam',
            fastaFile= {
                    'upstream': {'task': predictGenes,
                                 'port': 'genes'} ,
                    
                    } ,
            )

        
        runBlat= RunBlat(
            blatDB= '$KOBLATDB',
            db= 'ko',
            #pathToBlat= self.pathToBlat 
            fastaFile= {
                    'upstream': {'task': predictGenes,
                                 'port': 'genes'} ,
                    
                    } ,
            )


        #return [runBlastNr,runHmmer]
        #samples= glob.glob('/Users/kemal/phd/projects/periphyton/raw_sff/*.sff')
        return [runHmmer, runBlast]

    
    #def output(self):
    #    print 'finished'

    def run(self):
        print "running ..."


class Main1(luigi.Task):
    def requires(self):
        samples= glob.glob('/Users/kemal/phd/projects/periphyton/raw_sff/*.sff')
        qThreshold="20"
        return [MyWorkFlow(sample=sample,qThreshold=qThreshold) for sample in samples]

    def run():
        print 'running...'
    
class Main2(luigi.Task):
    def requires(self):
        projectIDs=["20","25","30"]
        #projectIDs=["pp"]
        return [CombineAlignments(projectID=projectID) for projectID in projectIDs]

    def run():
        print 'running...'




if __name__ == '__main__':
    luigi.run()

