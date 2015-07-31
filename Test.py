'''
Created on Jul 30, 2015

@author: dmh309
'''

from executioner import Executioner
from executioner.tasks import *
from executioner.octave import *
import logging

logging.basicConfig(level=logging.INFO)

#def parseOutput(content):
#    print("Parsing")
#    return { "result" : int(content) }
#
# with Executioner() as executioner:
#     executioner.add(CreateTempDir())
#     executioner.add(WriteFile("test.txt", "${test}"))
#     executioner.add(Format("test", "{:.0f}"))
#     executioner.add(Execute("echo '${test}'"))
#     executioner.add(CheckExitCode(ok=0))
#     executioner.add(ParseOutput(parseOutput))
#     executioner.add(DeleteTempDir())
#     print(executioner.evaluate({ "test": 25.5 }))
    
with Executioner() as executioner:
    executioner.onStart(Execute("python dtlz2.py"))
    executioner.add(Format("input", lambda x : " ".join(map(str, x))))
    executioner.add(WriteInput("${input}\n"))
    executioner.add(ParseLine(type=float))
    executioner.add(Return("output"))
    executioner.onComplete(WriteInput("\n"))
    
    print(executioner.evaluateBatch([{"input" : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                                     {"input" : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}]))

#executioner.add(StartOctaveEngine())
#executioner.add(EvaluateOctaveFunction("max", input=["test", "test"], output=["X"]))

