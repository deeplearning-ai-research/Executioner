'''
Created on Jul 30, 2015

@author: dhadka
'''

from executioner import Executioner, ResultList
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


# from executioner.salib import *
# from SALib.sample import saltelli
# from SALib.analyze import sobol
#    
# problem = {
#   'num_vars': 11,
#   'names': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11'], 
#   'bounds': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], 
#              [0, 1], [0, 1], [0, 1]]
# }
#    
# with Executioner() as executioner:
#     executioner.onStart(Execute("python dtlz2.py"))
#     executioner.add(WriteInput("${x1} ${x2} ${x3} ${x4} ${x5} ${x6} ${x7} ${x8} ${x9} ${x10} ${x11}\n"))
#     executioner.add(ParseLine(type=float, name=["y1", "y2"]))
#     executioner.onComplete(WriteInput("\n")) # send empty line to terminate process
#        
#     samples = saltelli.sample(problem, 1000, calc_second_order=True)
#     Y = executioner.evaluateBatch(SALibSamples(problem, samples))
#     sobol.analyze(problem, Y.to_nparray("y1"), print_to_console=True)

# def outputParser(input):
#     line = input.readline()
#     values = map(float, line.split())
#     return { "y1":values[0], "y2":values[1] }
#  
# with Executioner() as executioner:
#     executioner.onStart(Execute("python dtlz2_socket.py ${PORT}"))
#     executioner.onStart(Pause(1))
#     executioner.onStart(Connect(server=socket.gethostname(), port="${PORT}"))
#     executioner.add(Send("${x1} ${x2} ${x3} ${x4} ${x5} ${x6} ${x7} ${x8} ${x9} ${x10} ${x11}\n"))
#     executioner.add(Receive())
#     executioner.add(ParseOutput(outputParser))
#     executioner.onComplete(Send("\n"))
#     executioner.onComplete(Disconnect())
#     executioner.onError(PrintStderr())
#      
#     print(executioner.evaluate({"x1":0, "x2":0, "x3":0, "x4":0, "x5":0, "x6":0, "x7":0, "x8":0, "x9":0, "x10":0, "x11":0}))
#     print(executioner.evaluate({"x1":1, "x2":0, "x3":0, "x4":0, "x5":0, "x6":0, "x7":0, "x8":0, "x9":0, "x10":0, "x11":0}))

env = {}
ParseCSV("../../Results/cyberstar163.hpc.rcc.psu.edu-Cc1zt0/tabled_output.tab", delimiter="\t") \
    .get("row['value'] if row['name']=='plantNutrientUptake' and row['path']=='//bean/nitrate'", "a") \
    .run(env)
print(env)

WriteJSON({ "a":"${a}", "b":5, "c":"$c" }, "test.json", {"c":int}).run({"a":"hello", "c":2})