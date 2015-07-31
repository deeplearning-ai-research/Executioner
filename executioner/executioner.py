import os
import socket

class Executioner(object):
    
    def __init__(self):
        super(Executioner, self).__init__()
        self.tasks = []
        self.start_tasks = []
        self.complete_tasks = []
        self.running = False
        self.env = {}
        
    def __del__(self):
        if self.running:
            self.shutdown()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        if self.running:
            self.shutdown()
        return False
        
    def add(self, task):
        self.tasks.append(task)
        
    def onStart(self, task):
        self.start_tasks.append(task)
        
    def onComplete(self, task):
        self.complete_tasks.append(task)
    
    def start(self):
        self.env["SERVER"] = socket.gethostbyname(socket.getfqdn())
        self.env["WORK_DIR"] = os.path.abspath(".")
        
        for task in self.start_tasks:
            task.run(self.env)
        
        self.running = True
        
    def shutdown(self):
        for task in self.complete_tasks:
            task.run(self.env)
            
        self.running = False
    
    def evaluate(self, input={}, **kwargs):
        if not self.running:
            self.start()
        
        env = dict()
        env.update(self.env)
        env.update(input)
        env.update(kwargs)
        
        for task in self.tasks:
            task.run(env)
            
        return env
    
    def evaluateBatch(self, inputs=[], *args):
        all_inputs = []
        all_inputs.append(inputs)
        all_inputs.append(args)
        
        results = []
        
        for input in inputs:
            results.append(self.evaluate(input))
            
        return results