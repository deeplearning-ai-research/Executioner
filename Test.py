'''
Created on Jul 30, 2015

@author: dhadka
'''

from executioner import Executioner, ResultList
from executioner.tasks import *
from executioner.octave import *
import logging

#logging.basicConfig(level=logging.INFO)

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
    
# with Executioner() as executioner:
#     executioner.onStart(Execute("python dtlz2.py"))
#     executioner.add(Format("input", lambda x : " ".join(map(str, x))))
#     executioner.add(WriteInput("${input}\n"))
#     executioner.add(ParseLine(type=float))
#     executioner.add(Return("output"))
#     executioner.onComplete(WriteInput("\n"))
#      
#     print(executioner.evaluateBatch([{"input" : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
#                                      {"input" : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}]))


from executioner.salib import *
from SALib.sample import saltelli
from SALib.analyze import sobol
 
problem = {
  'num_vars': 11,
  'names': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11'], 
  'bounds': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], 
             [0, 1], [0, 1], [0, 1]]
}
 
with Executioner() as executioner:
    executioner.onStart(Execute("python dtlz2.py"))
    executioner.add(WriteInput("${x1} ${x2} ${x3} ${x4} ${x5} ${x6} ${x7} ${x8} ${x9} ${x10} ${x11}\n"))
    executioner.add(ParseLine(type=float, name=["y1", "y2"]))
    executioner.onComplete(WriteInput("\n")) # send empty line to terminate process
     
    samples = saltelli.sample(problem, 1000, calc_second_order=True)
    Y = executioner.evaluateBatch(SALibSamples(problem, samples))
    sobol.analyze(problem, np.array(Y[:,"y1"]), print_to_console=True)

