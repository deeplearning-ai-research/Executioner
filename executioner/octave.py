'''
Created on Jul 30, 2015
 
@author: dhadka
'''
 
import logging
import utils
from tasks import Task
from exceptions import TaskError
from oct2py import Oct2Py

# Note: When testing on Windows with GNU Octave-4.0.0, had to rename
# C:/Octave/Octave-4.0.0/bin/octave-cli.exe to octave.exe.
 
class StartOctaveEngine(Task):
    '''
    Starts the Octave engine.
    '''
     
    def __init__(self, **kwargs):
        super(StartOctaveEngine, self).__init__()
        self.kwargs = kwargs
         
    def run(self, env):
        logging.info("Starting Octave")
        env["OCTAVE_ENGINE"] = Oct2Py(**self.kwargs)
        logging.info("Successfully started Octave")
        

class StopOctaveEngine(Task):
    '''
    Stops the Octave engine.
    '''
    
    def __init__(self):
        super(StopOctaveEngine, self).__init__()
        
    def run(self, env):
        if "OCTAVE_ENGINE" not in env:
            logging.error("OCTAVE_ENGINE not defined")
            raise TaskError("OCTAVE_ENGINE not defined")
        
        env["OCTAVE_ENGINE"].exit()
        del env["OCTAVE_ENGINE"]
        logging.info("Exited Octave")
        

class AddOctavePath(Task):
    '''
    Adds a path to the Octave search path.
    '''
    
    def __init__(self, path):
        self.path = path
        
    def run(self, env):
        if "OCTAVE_ENGINE" not in env:
            logging.error("OCTAVE_ENGINE not defined")
            raise TaskError("OCTAVE_ENGINE not defined")
        
        logging.info("Adding " + str(self.path) + " to Octave's search path")
        env["OCTAVE_ENGINE"].addpath(self.path) 
        
        
class SetOctaveVar(Task):
    '''
    Sets the value of a variable in Octave.
    '''
    
    def __init__(self, key, value):
        super(SetOctaveVar, self).__init__()
        self.key = key
        self.value = value
        
    def run(self, env):
        if "OCTAVE_ENGINE" not in env:
            logging.error("OCTAVE_ENGINE not defined")
            raise TaskError("OCTAVE_ENGINE not defined")
         
        engine = env["OCTAVE_ENGINE"]
        env_key = utils.get_substitution_key(self.value, env)
        
        if env_key:
            engine.push(self.key, env[env_key])
            logging.info("Pushing variable " + self.key + " to Octave with value " + str(env[env_key]))
        elif isinstance(self.value, str) and self.value in env:
            engine.push(self.key, env[self.value])
            logging.info("Pushing variable " + self.key + " to Octave with value " + str(env[self.value]))
        elif isinstance(self.value, str):
            value = utils.substitute(self.value, env)
            engine.push(self.key, value)
            logging.info("Pushing variable " + self.key + " to Octave with value " + str(value))
        else:
            engine.push(self.key, self.value)
            logging.info("Pushing variable " + self.key + " to Octave with value " + str(self.value))
        
        
class GetOctaveVar(Task):
    '''
    Gets the value of a variable in Octave.
    '''
    
    def __init__(self, key, rename=None):
        super(GetOctaveVar, self).__init__()
        self.key = key
        self.rename = rename
        
    def run(self, env):
        if "OCTAVE_ENGINE" not in env:
            logging.error("OCTAVE_ENGINE not defined")
            raise TaskError("OCTAVE_ENGINE not defined")
        
        engine = env["OCTAVE_ENGINE"]
        name = self.key if self.rename is None else self.rename
        env[name] = engine.pull(self.key)
        logging.info("Pulled variable " + self.key + " from Octave with value " + str(env[name]))
     
     
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
        input_strs = []
        
        # If input argument is a variable, push into Octave's memory.
        # Otherwise, pass the input argument directly in the command.
        for arg in self.input:
            key = utils.get_substitution_key(arg, env)
            if key:
                engine.push(key, env[key])
                input_strs.append(key)
                logging.info("Pushing variable " + key + " to Octave with value " + str(env[key]))
            elif isinstance(arg, str) and arg in env:
                logging.info("Pushing variable " + arg + " to Octave with value " + str(env[arg]))
                engine.push(arg, env[arg])
                input_strs.append(arg)
            elif isinstance(arg, str):
                input_strs.append(utils.substitute(arg, env))
            else:
                input_strs.append(str(arg))
                
        # Build the command
        command = ""
        
        if len(self.output) > 0:
            command += "["
            command += ",".join(self.output)
            command += "] = "
            
        command += self.name
        command += "("
        command += ",".join(input_strs)
        command += ");"
        
        logging.info("Evaluating within Octave: " + command)
        engine.eval(command)
         
        for arg in self.output:
            env[arg] = engine.pull(arg)
            logging.info("Pulled variable " + arg + " from Octave with value " + str(env[arg]))
