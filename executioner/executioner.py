import os
import socket

class Executioner(object):
    
    def __init__(self):
        super(Executioner, self).__init__()
        self.tasks = []
        
    def add(self, task):
        self.tasks.append(task)
        
    def evaluate(self, input={}, **kwargs):
        base_env = {}
        base_env["SERVER"] = socket.gethostbyname(socket.getfqdn())
        base_env["WORK_DIR"] = os.path.abspath(".")
        
        env = dict()
        env.update(base_env)
        env.update(input)
        env.update(kwargs)
        
        for task in self.tasks:
            task.run(env)
            
        return env