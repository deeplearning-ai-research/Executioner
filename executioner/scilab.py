'''
Created on Jul 30, 2015

@author: dhadka
'''

from tasks import Task
from scilab import Scilab

#sci = Scilab()
#x = sci.rand(20, 20)
#y = x*x.transpose()
#y_inv = sci.inv(y)

class StartScilabEngine(Task):
    '''
    Starts Scilab engine.
    '''
    
    def __init__(self):
        super(StartScilabEngine, self).__init__()
        
    def run(self, env):
        env["SCILAB_ENGINE"] = Scilab()
    
class EvaluateScilabFunction(Task):
    '''
    Evaluates a Scilab function.
    '''
    
    def __init__(self, name, input=[], output=[]):
        super(EvaluateScilabFunction, self).__init__()
        self.name = name
        self.input = input
        self.output = output
        
    def run(self, env):
        pass
    