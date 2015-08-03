import os
import socket
import traceback

class ResultList(list):
    '''
    List of maps for storing the output of evaluateBatch.  Provides slicing
    to get specific fields from the output.
    '''
    
    def __getitem__(self, pos):
        if type(pos) is tuple:
            indices,keys = pos
            
            if type(indices) is slice:
                indices = xrange(*indices.indices(len(self)))
            elif type(indices) is int:
                indices = [indices]

            if type(keys) is list or type(keys) is tuple:
                result = ResultList()
                
                for i in indices:
                    submap = {}
                    
                    for key in keys:
                        submap[key] = super(ResultList, self).__getitem__(i)[key]
                    
                    result.append(submap)
                    
                return result
            else:
                result = []
                
                for i in indices:
                    result.append(super(ResultList, self).__getitem__(i)[keys])
                    
                return result
        else:
            super(ResultList, self).__getitem__(pos)

class Executioner(object):
    
    def __init__(self):
        super(Executioner, self).__init__()
        self.tasks = []
        self.start_tasks = []
        self.complete_tasks = []
        self.error_tasks = []
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
        
    def onError(self, task):
        self.error_tasks.append(task)
    
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
    
    def evaluate(self, input={}):
        if not self.running:
            self.start()
        
        try:
            env = dict()
            env.update(self.env)
            env.update(input)
            
            for task in self.tasks:
                task.run(env)
        except:
            print("Caught exception: ")
            traceback.print_exc()
            
            for task in self.error_tasks:
                task.run(env)
            
        return env
    
    def evaluateBatch(self, inputs=[]):        
        results = ResultList()
        
        for input in inputs:
            results.append(self.evaluate(input))
            
        return results