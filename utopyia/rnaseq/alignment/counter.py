import operator
import numpy as np
from pandas import DataFrame, Series, read_csv, concat

import pdb

class Counter(object):
    def __init__(self, sample_abundance_paths, output_abundance_path, level= "gene"):
        self.sample_abundance_paths = sample_abundance_paths
        self.output_abundance_path = output_abundance_path
        self.level = level

    def generate_counts(self):
        series_agg=[]
        sample_split_names= {}
        
        for sample, split_abundance_path in self.sample_abundance_paths.iteritems():
            for split_no, abundance_path in split_abundance_path.iteritems():
                sample_name= "%s_%s" %(sample, split_no)
                
                if sample not in sample_split_names:
                    sample_split_names[sample]= []
                
                sample_split_names[sample].append(sample_name)

                df_sample= read_csv(abundance_path, sep= "\t")               
                df_sample["genes"] = map(operator.itemgetter(0), 
                        Series(map(operator.itemgetter(1),  
                        df_sample['target_id'].str.split('|') )).str.split('.'))
                
                df_sample["transcripts"] = map(operator.itemgetter(0),
                        Series(map(operator.itemgetter(0),  
                        df_sample['target_id'].str.split('|') )).str.split('.'))           
                

                if self.level == "transcript":

                    df_transcripts= df_sample.groupby(["genes","transcripts"])["tpm"].apply(sum)
                    df_counts= df_transcripts

                else:
                    df_genes= df_sample.groupby("genes").sum()
                    df_counts= df_genes

                df_counts = df_counts.apply(np.ceil)["tpm"].to_frame(sample_name)

                series_agg.append(df_counts)
            
        count_dataframe = concat(series_agg, axis= 1, join= "outer")

        ### collating
        for sample, split_names in sample_split_names.iteritems():
            count_dataframe[sample] = count_dataframe[split_names].apply(np.sum, axis= 1)
            count_dataframe= count_dataframe.drop(split_names, axis= 1)
 
        count_dataframe.to_csv(self.output_abundance_path, sep="\t", index_label = self.level )
        return self.output_abundance_path


