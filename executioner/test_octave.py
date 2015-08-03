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
            executioner.onComplete(StopOctaveEngine())
            executioner.evaluate()
            self.assertIn("OCTAVE_ENGINE", executioner.env)
            
    def test_setget(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(SetOctaveVar("x", 100))
            executioner.add(GetOctaveVar("x", rename="xprime"))
            executioner.add(Assert("env[\"xprime\"] == 100"))
            executioner.onComplete(StopOctaveEngine())
            executioner.evaluate()
            
    def test_eval1(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(EvaluateOctaveFunction("max", input=["${a}", "${b}"], output=["x"]))
            executioner.add(Return("x"))
            executioner.onComplete(StopOctaveEngine())
            self.assertEquals(25, executioner.evaluate({"a":25, "b":15})["x"])
            
    def test_eval2(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(EvaluateOctaveFunction("max", input=["${a}", "35"], output=["x"]))
            executioner.add(Return("x"))
            executioner.onComplete(StopOctaveEngine())
            self.assertEquals(35, executioner.evaluate({"a":25})["x"])
            
    def test_types(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(SetOctaveVar("a", 25))
            executioner.add(SetOctaveVar("c", "${b}"))
            executioner.add(EvaluateOctaveFunction("max", input=["a", "c"], output=["x"]))
            executioner.add(Return("x"))
            executioner.onComplete(StopOctaveEngine())
            self.assertEquals(30, executioner.evaluate({"b":30})["x"])
            
    def test_error(self):
        with Executioner() as executioner:
            executioner.onStart(StartOctaveEngine())
            executioner.add(EvaluateOctaveFunction("doesnotexist", input=[25, 35], output=["x"]))
            executioner.onComplete(StopOctaveEngine())
            executioner.evaluate()
            
            self.assertTrue(executioner.last_error is not None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()