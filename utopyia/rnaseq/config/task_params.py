# merge split decompress
compression_method= "bzip"
max_n_seq=1000

# project
project_name= "mock"
replication_level= "replicate"
fname_column_separator= "_"
fname_read_index= -1
fname_order_index= 0
fname_extension= ".bz2" if compression_method == "bzip" else ".gz"

# sbatch
job_id= "snic2016-1-184"
resource_type= "core"
n_resource= 8
run_time= "01:00:00"
job_name= "rnaseq_pipeline"
e_mail= "kemal.sanli@scilifelab.se"

