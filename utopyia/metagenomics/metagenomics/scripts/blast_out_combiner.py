# input is a list of tab separated blast outputs belonging to the same sampling site eg. nr/nt blast, kegg blast, rRNA blast. 
# column 1: query (read)
# column 2: target (function)

# kegg= K12826:c5633d2b0387128c23ac7f6504b775d7
# gi1= 118370424
# swissprot= Q9R9N3
# swissprot2= sp|Q9SKU1|CLC1_ARATH
# cazy= ADQ05660:alpha-glucan 
# 

def extractReadAnnotations(blastOutputFiles):
    Inputs={}
    for blastOut in blastOutputFiles:
        
        
        bOut=open(blastOut)    
        Reads={}
        Functions={}

        for line in bOut:
            cols=line.rstrip('\n').split('\t')
            read= cols[0]
            function= cols[1]

            # read identifiers must be extended by '_' (underscore) sign if more than 1 sequence is representing the same read.
            # function should be separated by '|' (bar).

            read= read.split('_')[0]
            
            #if '|' in function:
            #function=function.split('|')
            
            #for f in functions:
            if ':' in function:
                function=function.split(':')[0].split('.')[0]
                if f not in Functions:
                    Functions[function]=[]
                Functions[function].append(read)
            else:
                if function not in Functions:
                    Functions[function]=[]
                
                Functions[function].append(read)


            if read not in Reads:
                Reads[read] = []
            

            #Reads[read] += (kos.split(':')[0] for kos in functions)
            Reads[read] += function
        
        Inputs[fileName]= (Reads, Functions)
        
    
    all_reads=set()
    for f in blastOutputFiles:
        all_reads=all_reads.union(set(Inputs[f][0].keys()))

    all_reads=list(all_reads)

def printReads(all_reads):
    for read in all_reads[:5]:
        for f in input_files:
            try:
                print '###### '+ f +' #####'
                print read,':\t', Inputs[f][0][read]
            except:
                print
        print '#############'
        print '#############'


def printFunctions(all_reads):
    for f in input_files:
        print '####################'
        print '####################'
        for k,v in Inputs[f][1].iteritems():

            print f
            print k,':\t', set(v)
            print 




