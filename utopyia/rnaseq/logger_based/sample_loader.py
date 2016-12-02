import glob, os
from collections import OrderedDict
import pdb

class Replicate(object):
    def __init__(self, replicate_dir, lane_index=0, read_index=-1, fname_convention_splitter="_"):
        self.replicate_dir= replicate_dir
        self.lane_index= lane_index
        self.read_index= read_index
        self.fname_convention_splitter= fname_convention_splitter
    
    @property
    def lane_pairs(self):
        files= glob.glob(os.path.join(self.replicate_dir,"*.gz"))
        pairs= {}
        for compressed_fastq_file in files:
            metadata_fields = os.path.basename(compressed_fastq_file).split(self.fname_convention_splitter)
            lane= int(metadata_fields[self.lane_index])
            pair_id= int(metadata_fields[self.read_index].replace(".fastq.gz",""))
            
            if lane not in pairs:
                pairs[lane]= [None, None]
            
            pairs[lane][pair_id-1] = compressed_fastq_file
       
        return OrderedDict(sorted(pairs.items()))


class Sample(object):
    def __init__(self):
        self.replicates= []

    def add_replicate(self, replicate_dir):
        rep= Replicate(replicate_dir)
        self.replicates.append(rep)




class SampleLoader(object):
    def __init__(self, project_dir):
        self.project_dir= project_dir
        self.add_samples()
        
    
    @property
    def samples(self):
        samples={}
        all_files = [(a,b,[i for i in c if i.endswith(".gz")]) for a,b,c in os.walk(self.project_dir)]
        for branch in all_files:
            if branch[1] == []:
                files= branch[2]
                sample_replicate= os.path.split(branch[0])
                            
                sample_dir= sample_replicate[0].strip("/")
                replicate_dir= os.path.join(self.project_dir, branch[0])
                
                if sample_dir not in samples:
                    samples[sample_dir]= Sample()
                samples[sample_dir].add_replicate(replicate_dir)
        return samples


    def yield_lane_pairs(self):
        for sample_dir, sample in self.samples.iteritems():
            for replicate in sample.replicates:
                yield (os.path.basename(sample_dir), os.path.basename(replicate.replicate_dir), replicate.lane_pairs.iteritems())



