# merge split decompress
compression_method= "tar.gz"
max_n_seq= 1000000
#max_n_seq= 5000

# project
project_name= "low_carb"
replication_level= "replicate"
fname_column_separator= "_"
fname_read_index= -1
fname_order_index= 1
#fname_order_index= 0
if compression_method == "bzip":
    fname_extension= ".bz2" 
elif compression_method == "gzip":
    fname_extension = ".gz"
elif compression_method == "tar.gz":
    fname_extension = ".tar.gz"
# sbatch
job_id= "snic2016-1-184"
resource_type= "core"
n_resource= 5
run_time= "10:00:00"
job_name= "rnaseq_pipeline"
e_mail= "kemal.sanli@scilifelab.se"

