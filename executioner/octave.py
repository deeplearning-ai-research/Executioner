'''
Created on Jul 30, 2015

@author: dhadka
'''

import logging
from tasks import Task
from exceptions import TaskError
from oct2py import Oct2Py

class StartOctaveEngine(Task):
    '''
    Starts the Octave engine.
    '''
    
    def __init__(self):
        super(StartOctaveEngine, self).__init__()
        
    def run(self, env):
        env["OCTAVE_ENGINE"] = Oct2Py()
    
class EvaluateOctaveFunction(Task):
    '''
    Evaluates an Octave function.
    '''
    
    def __init__(self, name, input=[], output=[]):
        super(EvaluateOctaveFunction, self).__init__()
        self.name = name
        self.input = input
        self.output = output
        
    def run(self, env):
        if "OCTAVE_ENGINE" not in env:
            logging.error("OCTAVE_ENGINE not defined")
            raise TaskError("OCTAVE_ENGINE not defined")
        
        engine = env["OCTAVE_ENGINE"]
        
        for arg in self.input:
            engine.push(arg, env[arg])
        
        command = "["
        command += ",".join(self.output)
        command += "] + "
        command += self.name
        command += "("
        command += ",".join(input)
        command += ")"
        
        engine.eval(command)
        
        for arg in self.output:
            env[arg] = engine.pull(arg)
            
        