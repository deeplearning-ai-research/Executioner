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
     
    def __init__(self):
        super(StartOctaveEngine, self).__init__()
         
    def run(self, env):
        logging.info("Starting Octave")
        env["OCTAVE_ENGINE"] = Oct2Py()
        logging.info("Successfully started Octave")
     
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
            elif type(arg) is str and arg in env:
                logging.info("Pushing variable " + arg + " to Octave with value " + str(env[key]))
                engine.push(arg, env[arg])
                input_strs.append(arg)
            else:
                input_strs.append(utils.substitute(arg, env))
         
        command = "["
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
