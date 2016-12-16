from fabric.api import local, env, run, cd


  

def setenv():
    env.user = "adilm"
    env.hosts= ["adilm@tintin.uppmax.uu.se"]


def push():
    local("cd ~/repos/utopyia && git push")

def pull():
    run("cd /home/adilm/repos/utopyia &&git pull")



push()
setenv()
pull()

