from fabric.api import run, env, hosts, sudo

env.hosts = ['codeways.org']
env.user = 'chris'

@hosts('codeways.org')
def run_development_server():
    sudo('uname -s', user='root')
