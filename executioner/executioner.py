import os
import socket
import traceback

class ResultList(list):
    '''
    List of maps for storing the output of evaluateBatch.  Provides slicing
    to get specific fields from the output.
    '''
    
    def to_list(self, key=None, index=0):
        result = []
        
        if len(self) == 0:
            return result
        
        if key is None:
            if len(self[0].keys()) > 1:
                raise ValueError("Can not convert ResultList to list that contains more than one key")
            else:
                key = list(self[0].keys())[0]
            
        for i in range(len(self)):
            value = super(ResultList, self).__getitem__(i)[key]
            result.append(value[index] if type(value) is list else value)
                
        return result
    
    def to_nparray(self, keys=None, index=0):
        import numpy
        
        if len(self) == 0:
            return numpy.empty([0])
        
        if keys is None:
            keys = self[0].keys()
            
        if type(keys) is str:
            keys = [keys]
            
        if type(keys) is set:
            keys = list(keys)
    
        if len(keys) == 1:
            key = keys[0]
            result = numpy.empty([len(self)], dtype=numpy.dtype(type(self[0][key])))
            
            for i, env in enumerate(self):
                result[i] = env[key][index] if type(env[key]) is list else env[key]
        else:
            dt = { "names" : keys, "formats" : [numpy.dtype(type(self[0][key])) for key in keys] }
            result = numpy.empty([len(self)], dtype=dt)
    
            for i, env in enumerate(self):
                result[i] = tuple(env[key][index] if type(env[key]) is list else env[key] for key in keys)
        
        return result
    
    def __getitem__(self, pos):
        if type(pos) is tuple:
            indices,keys = pos
            
            if type(indices) is slice:
                indices = xrange(*indices.indices(len(self)))
            elif type(indices) is int:
                indices = [indices]
                
            if type(keys) is not list and type(keys) is not tuple:
                keys = [keys]

            result = ResultList()
                
            for i in indices:
                submap = {}
                    
                for key in keys:
                    submap[key] = super(ResultList, self).__getitem__(i)[key]
                    
                result.append(submap)
                    
            return result
        elif type(pos) is str:
            return self.to_list(pos)
        else:
            return super(ResultList, self).__getitem__(pos)

class Executioner(object):
    
    def __init__(self):
        super(Executioner, self).__init__()
        self.tasks = []
        self.start_tasks = []
        self.complete_tasks = []
        self.error_tasks = []
        self.running = False
        self.env = {}
        self.last_error = None
        
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
        except Exception as ex:
            self.last_error = ex
            traceback.print_exc()
            
            for task in self.error_tasks:
                task.run(env)
            
            # allow assertions to propogate for unit testing
            if type(ex) is AssertionError:
                raise
            
        return env
    
    def evaluateBatch(self, inputs=[]):        
        results = ResultList()
        
        for input in inputs:
            results.append(self.evaluate(input))
            
        return results
    