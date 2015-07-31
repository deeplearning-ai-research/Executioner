'''
Created on Jul 31, 2015

@author: dhadka
'''
import unittest
from . import Executioner
from tasks import *
from salib import *

class TestSALib(unittest.TestCase):

    def test_sobol(self):
        with Executioner() as executioner:
            
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
