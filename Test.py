'''
Created on Jul 30, 2015

@author: dmh309
'''

from executioner import Executioner
from executioner.tasks import *
import logging

logging.basicConfig(level=logging.INFO)

def parseOutput(content):
    print("Parsing")
    return { "result" : content }


executioner = Executioner()
executioner.add(CreateTempDir())
executioner.add(WriteFile("test.txt", "${test}"))
executioner.add(Format("test", "{:.0f}"))
executioner.add(Execute("echo hello world"))
executioner.add(CheckExitCode(ok=0))
executioner.add(ParseOutput(parseOutput))
executioner.add(DeleteTempDir())

print(executioner.evaluate({ "test": 25.5 }))
