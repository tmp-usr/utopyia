import csv,glob
import os 
import pickle

import luigi

from pandas import DataFrame, Series, concat, merge
from helpers import run_cmd
from dependencymixin import DependencyMetaTask
from Bio import SeqIO
from collections import namedtuple



class CombineAlignments(DependencyMetaTask):
    """
    as far as I could find mothur does not allow changing output file names. this was annoying. use any of the other command line trimming tools. FastQPolish is preferred here.

    """
    projectID= luigi.Parameter()
    #blastOutputs= luigi.Parameter()
    #hmmDB= luigi.Parameter()
    #db= luigi.Parameter()
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
        #fastaFile=self.get_input('fastaFile')
        #db=self.get_input('db')
        #dbs= {os.path.basename(f).split('.')[-2]:luigi.LocalTarget('tables/%s.tsv' 
        #    % os.path.basename(f).split('.')[-2]) for f in self.blastOutputFiles}
        
        self.blastOutputFiles= glob.glob('alignment/hmmer/*%s*.blast'% self.get_input('projectID'))
        self.blastOutputFiles+= glob.glob('alignment/blast/*/*%s*.blast'% self.get_input('projectID'))
        
        dbs= {os.path.basename(f).split('.')[-2]:
                luigi.LocalTarget('tables/%s.%s.tsv' % 
            (self.get_input('projectID'), os.path.basename(f).split('.')[-2])) for f in self.blastOutputFiles}

        outputs= { 'reads': 
                    luigi.LocalTarget(
                       'alignment/combined/reads.txt'),
                 'functions':
                    luigi.LocalTarget(
                       'alignment/combined/functions.txt') ,
                

                 #'tables':
                 #    luigi.LocalTarget(
                 #      'counts/'),

                  #'discard': 
                  #  luigi.LocalTarget(
                  # 'discard/' +  os.path.basename(self.get_input('fastqFile').path).replace('.fastq','.discard.fastq'))
                }
        
        outputs.update(dbs)
        return outputs

        #print 'finished'
        #    return luigi.LocalTarget("trimmed/%s.fasta" %self.sample)
    
    def extractReadAnnotations(self, e_value_t=1e-5, perc_identity_t=60):
        """
            blast output filtering also takes place here.
        """


        
        self.Inputs={}
        self.SampleReads={}
        self.SampleFunctions={}
        
        self.DBFunctions={}

        for blastOut in self.blastOutputFiles:
            
            bOut=open(blastOut)    
            
            sample= os.path.basename(blastOut).split('.')[0]
            db= os.path.basename(blastOut).split('.')[-2]


            if db not in self.SampleFunctions:
                self.SampleFunctions[db]= {}

            if sample not in self.SampleFunctions[db]:
                self.SampleFunctions[db][sample]= {}

            if sample not in self.SampleReads:
                self.SampleReads[sample]= {}
            


            #Reads={}
            Functions={}

            for line in bOut:
                cols=line.rstrip('\n').split('\t')
                read= cols[0]
                
                function= cols[1].split('.')[0]
                kegg= function.split(':')
                function= kegg[0]
                md5=1
                if len(kegg) >1:
                    md5= kegg[-1]
                
                if 'kegg' in db and not function.startswith('K'):
                    continue


                perc= cols[2]
                e_value= cols[10]
    
               
               ### a confirmatory filtering takes place here 
                try:
                    if float(perc) < perc_identity_t:
                        continue
                except:
                    pass

                if float(e_value) > e_value_t:
                    continue


                #print function
                # read identifiers must be extended by '_' (underscore) sign if more than 1 sequence is representing the same read.
                # function should be separated by '|' (bar).

                read= read.split('_')[0]
               
                if read == '':
                    continue


                #if '|' in function:
                #function=function.split('|')
                
                #for f in functions:
                #    if f not in Functions:
                #        Functions[function]=[]
                #    Functions[function].append(read)
                
                #if read not in Reads:
                #    Reads[read] = []

               
                #if function not in self.DBFunctions[db]:
                #    self.SampleFunctions[db]

                
                if function not in self.SampleFunctions[db][sample]:
                    self.SampleFunctions[db][sample][function]={}
                                     
                #print sample, self.SampleFunctions[db][sample]
                alignment= (md5,e_value,perc)

                if read not in self.SampleFunctions[db][sample][function]:
                    self.SampleFunctions[db][sample][function][read]=alignment                 
                else:
                    prev_md5,prev_e_value, prev_perc =  self.SampleFunctions[db][sample][function][read]
                    if prev_e_value > alignment[1]:
                        self.SampleFunctions[db][sample][function][read]= alignment

                    else:
                        if prev_e_value == alignment[1]:
                            if prev_perc < alignment[2]:
                                self.SampleFunctions[db][sample][function][read]= alignment
                        
                #print function
                if read not in self.SampleReads[sample]:
                    self.SampleReads[sample][read]= []
                
                #if read not in Reads:
                #    Reads[read] = []
                

                #Reads[read] += (kos.split(':')[0] for kos in functions)
                self.SampleReads[sample][read].append(function)
                #Reads[read].append(function)
            
            

            #for k,v in Functions.iteritems():

            #self.Inputs[blastOut]= (Reads, Functions)
        
        


        #self.all_reads=set()
        #for f in blastOutputFiles:
        #    self.all_reads=self.all_reads.union(set(self.Inputs[f][0].keys()))

        #self.all_reads=list(self.all_reads)
        #print len(self.all_reads)

    def printReads(self): 
    # use this later, count tables will be used for the rest of the analysis
                        
        for sample, Reads in self.SampleReads.iteritems():
            print sample
            for read, functions in Reads.iteritems():
                print read+":%s"% ';'.join(set(functions))

    #    for read in self.all_reads:
    #        for f in input_files:
    #            if read in self.Inputs[f][0]:
    #                ann= self.Inputs[f][0][read]
    #                print ann
    #                #anno=';'.join(ann)
    #                #if 'PF' in anno and 'K' in anno:
    #                #    print read, ann
    #                #print '###### '+ f +' #####'
    #                #print read,':\t', len(ann)
    #        #print '#############'
    #        #print '#############'



    def printFunctions(self):# write count table here
        for db, Samples in self.SampleFunctions.iteritems():
            if db == 'nr':
                continue
            #df= DataFrame()
            dfs=[]
            fOut= self.output()[db].path
            fDmpOutDir=  '%s/md5/' %os.path.dirname(fOut)
            if not os.path.exists(fDmpOutDir):
                os.makedirs(fDmpOutDir)

        #with open(fTrim,'w') as trim:
        #    SeqIO.convert(sffFile, "sff-trim", fasta, "fasta")
            
            
            
            for sample, Functions in Samples.iteritems():
                #print sample
                #print Functions
                index= Functions.keys()
                values= [len(Reads.keys()) for Reads in Functions.values()]
                #print index
                #print values
                sampleData= DataFrame(values, index= Functions.keys(), columns=[sample] )
            
                ## dumping corresponding reads and m5nr md5s associated with the found functions  
                #Functions={k:v[0] for k,v in Functions.iteritems()}
                pickle.dump(Functions, open('%s/md5/%s.dmp' %(os.path.dirname(fOut),sample), 'w'))
                #print sampleData
                #print sampleData[sample]
                #df= concat([df,sampleData], join='inner')
                dfs.append(sampleData)
                #print sampleData
                #df.append(sampleData, ignore_index=True)
            df_all=dfs[0].join(dfs[1:],how='outer').fillna(0)
            df_all.index.name='Name'
            cols= sorted(df_all.columns.tolist())
            df_all= df_all[cols]
            #df_all.index_col='Function'
            df_all.to_csv(fOut, sep='\t', float_format="%d")

                #for function, reads in Functions.iteritems():
                    
                #    print '\t'.join([sample,function,str(len(reads))])
    
    
    
    def printAnnotationStats(self):
        AllFunctions={}
        AllReads={}
        
        #for sample, Functions in self.SampleFunctions.iteritems():
        #    AllFunctions.update(Functions)
    
        for sample, Reads in self.SampleReads.iteritems():
            AllReads.update(Reads)

        count= len(AllReads.keys())
        perc= count* 100 /float(6000)
        print "Total %s reads (%s percent)" %(count, perc) 
        #for k,v in AllReads.iteritems():
        #    print k, v
        #AllFunctions[]
    
    #    for f in input_files:
    #        print '####################'
    #        print '####################'
    #        for k,v in self.Inputs[f][1].iteritems():

    #            print f
    #            print k,':\t', set(v)
    #            print 
    
    def combine(self):
        #mothurCmd = "\"#trim.seqs(fasta=%s, qfile=%s, qwindowaverage=%s, minlength=%s)\"" %(fastaFile, qualFile, qThreshold, minSeqLen)
        #mothurLoc= "/Users/kemal/mothur/mothur"
        #return [ mothurLoc , mothurCmd ]  
        fReads= self.output()['reads'].path
        fFunctions= self.output()['functions'].path
        
        if not os.path.exists(os.path.dirname(fReads)):
            os.makedirs(os.path.dirname(fReads))
        
        if not os.path.exists(os.path.dirname(fFunctions)):
            os.makedirs(os.path.dirname(fFunctions))

        #fDiscard= self.output()['discard'].path
        
        #if not os.path.exists(os.path.dirname(fDiscard)):
        #    os.makedirs(os.path.dirname(fDiscard))
        #blastOutputFiles= glob.glob('alignment/blast/*/*30*.blast')

        #print blastOutputFiles
        self.extractReadAnnotations()
        #self.printReads()
        #self.printFunctions()
        self.printAnnotationStats() 

    def run(self):
        print '==== Combining Blast Outputs ===='
        print self.get_input('projectID') 
        self.combine() 
        

