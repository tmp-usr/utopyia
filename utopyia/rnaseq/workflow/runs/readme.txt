1. align (compressed|decompressed) ==> generate_counts
2. merge ==> align (compressed|decompressed) ==> generate_counts
3. split ==> align (compressed|decompressed) ==> generate_counts
3. merge ==> split ==> align (compressed|decompressed) ==> generate_counts



a. merge: requires a fastq_file_container or file paths in a given order (important). outputs a file or a container with two files only
a.i. merge_containers: requires a container to be merged and returns the new containers extending the previous name with merged

This process updates the previous state of self.all_fastq_containers. which now contains the new names and the file paths.


b. split: requires a fastq_file
b.i. split_container: requires a container of fastq_pairs to be split and returns the new containers extending the previous name with the order of the split file name.

This process updates the previous state of self.all_fastq_containers. which now contains the new names and the file paths.

c. alignment input providers contain simply file paths for individual pair




