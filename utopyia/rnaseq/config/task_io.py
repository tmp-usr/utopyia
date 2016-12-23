import os
import copy

import pdb


######## TODO: Fill in raw_data_dir, tmp_dir, output_dir
#              reference_genome_dir, if required change 
#              the reference genome index params. 
#        TODO: If the pipelines will be extended in the future
#              the new input and output files should be extended
#              from the template dictionary "task" below.

### Project
# local
#project_dir=  "/Users/kemal/Desktop/postdoc/projects/mock_low_carb"

# server
project_dir= "/home/adilm/projects/mock_low_carb"
###
raw_data_dir= os.path.join(project_dir, "raw_data")
tmp_dir= os.environ["SNIC_TMP"]
#tmp_dir= os.path.join(project_dir, "tmp")
output_dir= os.path.join(project_dir, "outputs")


###
alignment_tmp_dir= os.path.join(output_dir, "alignment")
alignment_output_dir= os.path.join(output_dir, "alignment")


###
reference_genome_dir= "/home/adilm/projects/reference_genomes/human"

kallisto_genome_index= os.path.join(reference_genome_dir, "hg19.kallisto.GRCh38.index")

star_genome_dir= os.path.join(reference_genome_dir, "genome_dir")
star_genome_fasta_path= os.path.join(reference_genome_dir, "GRCh38.d1.vd1.fa")
star_genome_gtf_file= os.path.join(reference_genome_dir, "gencode.v22.annotation.gtf")
###



task= {
        "root_dir":"",
        "input_files": {},
        "input_dirs": {},
        "tmp_files": {},
        "tmp_dirs":   {},
        "output_files":{},
        "output_dirs":{}
       }


def gen_project_io():
    project= copy.deepcopy(task)
    project["root_dir"]= raw_data_dir
    return project

#### merge params
def gen_merge_io(fastq_container):
    # initiating the empty dictionary
    merge= copy.deepcopy(task)

    ### to be used with the fastq_container_splitter
    merge["root_dir"]= os.path.join(tmp_dir, "merge")
    merge["tmp_dirs"]["merge_dir"]= os.path.join(merge["root_dir"], fastq_container.name)
        
    return merge



#### split params
def gen_split_io(fastq_container):
    # initiating the empty dictionary
    split = copy.deepcopy(task)
    
    ### to be used with the fastq_container_splitter
    split["root_dir"] = os.path.join(tmp_dir, "split")
    split["tmp_dirs"]["split_dir"]= os.path.join(split["root_dir"], fastq_container.name)

    return split


def gen_count_io(sample_abundance_dir):
    count= copy.deepcopy(task)

    count["root_dir"] = alignment_output_dir
    count["input_files"]["abundance"]= os.path.join(sample_abundance_dir, "abundance.tsv" )
    
    count["output_files"]["gene"]= os.path.join(alignment_output_dir, "gene_counts.tsv")
    count["output_files"]["transcript"]= os.path.join(alignment_output_dir, "transcript_counts.tsv")
    

    return count


#### align params
def gen_align_io(method, fastq_container, reads1_path, reads2_path, file_learner):
    # initiating the empty dictionary
    align= copy.deepcopy(task)

    align["root_dir"]= alignment_tmp_dir
    align["input_files"]["reads1"]= reads1_path
    align["input_files"]["reads2"]= reads2_path
    file_learner.set_file(reads1_path)
    
    align["output_dirs"]["output_dir"]= os.path.join(alignment_output_dir, fastq_container.name, file_learner.trim_extension())

    if method == "kallisto":
        align["input_files"]["genome_index"]= kallisto_genome_index

    
    elif method == "star":
        align["input_dirs"]["genome_dir1"] = star_genome_dir
        align["input_files"]["genome_fasta_path"]= star_genome_fasta_path
        align["input_files"]["gtf_file"]= star_genome_gtf_file
        
        align["tmp_dirs"]["genome_dir2"] = os.path.join(alignment_tmp_dir, "genome_dir2", fastq_container.name)
        align["tmp_dirs"]["tmp_output_dir1"]= os.path.join(alignment_tmp_dir, "tmp_output_dir1", fastq_container.name)
        align["tmp_dirs"]["tmp_output_dir2"]= os.path.join(alignment_tmp_dir, "tmp_output_dir2", fastq_container.name)
        
        
        align["output_files"]["sj_out"]= os.path.join(align["output_dirs"]["output_dir"], "_SJ.out.tab")
        align["output_files"]["bam_out"]= os.path.join(align["output_dirs"]["output_dir"], "_Aligned.sortedByCoord.out.bam")
        align["output_files"]["count_out"]= os.path.join(align["output_dirs"]["output_dir"], "count.txt")

    # the below parameter does not refer to a file
    # in idiotic software tools like star, the ultra fast aligner
    # authors of the tool sometimes do not allow you to 
    # manually enter output names and they enforce you to
    # have their long suffixes for the output files.

        align["output_files"]["output_prefix"]=  os.path.join(align["output_dirs"]["output_dir"], "_")

    return align
