import subprocess

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE)
    #ret_code = p.wait()
    output = p.communicate()[0]
    return output
