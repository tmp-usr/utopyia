import gzip, bz2
import tarfile
import subprocess
import tempfile


class FastQDecompressor(object):
    def __init__(self, compressed_file_path, compression_method, 
            return_type, decompressed_file_path= None):
        self.compressed_file_path = compressed_file_path
        self.compression_method= compression_method
        self.return_type= return_type
        self.decompressed_file_path= decompressed_file_path

    def decompress(self):
        if self.compression_method == "gzip":
            handle= gzip.open(self.compressed_file_path, "rb")
        
        elif self.compression_method == "tar.gz":
            tmp_file= tempfile.NamedTemporaryFile(delete= False)
            command_line= "tar -xzf %s > %s" %(self.compressed_file_path, tmp_file.name)
            p= subprocess.Popen(command_line, shell= True).wait()
            handle= open(tmp_file.name, "r")

        elif self.compression_method == "bzip":
            tmp_file= tempfile.NamedTemporaryFile(delete= False)
            command_line= "bzcat -dkf %s > %s" %(self.compressed_file_path, tmp_file.name)
            p= subprocess.Popen(command_line, shell= True).wait()
            handle= open(tmp_file.name, "r")
            
            ### below line does not work. so we have to use the above 
            ### workaround. which makes things slower than they are.
            
            #handle= bz2.BZ2File(self.compressed_file_path)

        if self.return_type == "stream":
            return handle

        elif self.return_type == "file":
            with open(self.decompressed_file_path, "w") as decompressed_file:
                decompressed_file.write(handle.read())
            return self.decompressed_file_path


