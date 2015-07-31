'''
Created on Jul 31, 2015

@author: dhadka
'''
import unittest
from . import Executioner
from tasks import *
from octave import *
import logging

logging.basicConfig(level=logging.INFO)

class TestOctave(unittest.TestCase):

    def test_startup(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.evaluate()
            self.assertIn("OCTAVE_ENGINE", executioner.env)
            
    def test_eval1(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(EvaluateOctaveFunction("max", input=["${a}", "${b}"], output=["x"]))
            executioner.add(Return("x"))
            self.assertEquals(25, executioner.evaluate({"a":25, "b":15})["x"])
            
    def test_eval2(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(EvaluateOctaveFunction("max", input=["${a}", "35"], output=["x"]))
            executioner.add(Return("x"))
            self.assertEquals(35, executioner.evaluate({"a":25})["x"])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()