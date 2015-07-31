'''
Created on Jul 30, 2015

@author: dhadka
'''

import os
import shutil
from string import Template

def copytree(src, dst):
    '''
    Similar to shutil.copytree, except it works even when the dst folder exists.
    '''
    
    if not os.path.exists(dst):
        os.makedirs(dst)
        
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isdir(s):
            copytree(s, d)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
                
def substitute(str, env):
    template = Template(str)
    return template.safe_substitute(env)

def substitutetree(src, env):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        
        if os.path.isdir(s):
            substitutetree(s, env)
        else:
            with open(s) as file:
                template = Template(file.read())
                
            with open(s, 'w') as file:
                file.write(template.safe_substitute(env))
                
def redirect(stream, env, name):
    while True:
        line = stream.readline()
        
        if not line:
            break

        env[name].seek(0, os.SEEK_END)
        env[name].write(line)
        print(env[name].getvalue())