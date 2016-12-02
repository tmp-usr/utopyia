import subprocess
from subprocess import PIPE, STDOUT
import time
def run():
    command_line = 'squeue | grep adilm'
    p = subprocess.Popen(command_line, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    out= p.stdout.read()
    ### log
    while out != "":
        time.sleep(5)
        
        print "hamza"
        p = subprocess.Popen(command_line, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        out = p.stdout.read()
        print out

run()

