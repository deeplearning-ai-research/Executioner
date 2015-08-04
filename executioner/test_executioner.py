'''
Created on Aug 4, 2015

@author: dmh309
'''
import unittest
import tempfile
import shutil
import logging
from . import Executioner
from tasks import *

logging.basicConfig(level=logging.INFO)

class Test(unittest.TestCase):


    def test_xml(self):
        input = "<root><key name=\"y1\"><value1>1</value1><value2>2</value2></key><key name=\"y2\"><value1>3</value1><value2>4</value2></key></root>"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseXML(tmp_file).get(".//key[@name='y1']/value1", "y1", float).get(".//key[@name='y2']/value2", "y2", float).run(env)
        self.assertEquals(env["y1"], 1)
        self.assertEquals(env["y2"], 4)
        
        os.remove(tmp_file)
        
    def test_xml_findall(self):
        input = "<root><key name=\"y1\"><value>1</value><value>2</value></key><key name=\"y2\"><value>3</value><value>4</value></key></root>"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseXML(tmp_file).get(".//key[@name='y1']/value", "y1", float).get(".//key[@name='y2']/value", "y2", float).run(env)
        self.assertEquals(env["y1"], [1,2])
        self.assertEquals(env["y2"], [3,4])
        
        os.remove(tmp_file)
        
    def test_json(self):
        input = "{ \"root\": { \"y1\" : [1, 2], \"y2\" : [3, 4] } }"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseJSON(tmp_file).get("root.y1[0]", "y1", float).get("root.y2[1]", "y2", float).run(env)
        self.assertEquals(env["y1"], 1)
        self.assertEquals(env["y2"], 4)
        
        os.remove(tmp_file)
        
    def test_json_findall(self):
        input = "{ \"root\": { \"y1\" : [1, 2], \"y2\" : [3, 4] } }"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseJSON(tmp_file).get("root.y1", "y1", float).get("root.y2", "y2", float).run(env)
        self.assertEquals(env["y1"], [1, 2])
        self.assertEquals(env["y2"], [3, 4])
        
        os.remove(tmp_file)
        
    def test_csv(self):
        input = "y1,y2\n1,3\n2,4"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseCSV(tmp_file).get("row[1]/@y1", "y1", float).get("row[2]/@y2", "y2", float).run(env)
        self.assertEquals(env["y1"], 1)
        self.assertEquals(env["y2"], 4)
        
        os.remove(tmp_file)
        
    def test_csv_findall(self):
        input = "y1,y2\n1,3\n2,4"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseCSV(tmp_file).get("row/@y1", "y1", float).get("row/@y2", "y2", float).run(env)
        self.assertEquals(env["y1"], [1, 2])
        self.assertEquals(env["y2"], [3, 4])
        
        os.remove(tmp_file)
        
    def test_csv_tabs(self):
        input = "y1\ty2\n1\t3\n2\t4"
        tmp_file = tempfile.mktemp()
        
        with open(tmp_file, "w") as f:
            f.write(input)
        
        env = {}
        ParseCSV(tmp_file, delimiter="\t").get("row[1]/@y1", "y1", float).get("row[2]/@y2", "y2", float).run(env)
        self.assertEquals(env["y1"], 1)
        self.assertEquals(env["y2"], 4)
        
        os.remove(tmp_file)
        
    def test_substitute(self):
        tmp_dir = tempfile.mkdtemp()
        print(tmp_dir)
        tmp_file1 = tempfile.mktemp(suffix=".txt", dir=tmp_dir)
        tmp_file2 = tempfile.mktemp(suffix=".dat", dir=tmp_dir)
        
        with open(tmp_file1, "w") as f:
            f.write("${val}")
            
        with open(tmp_file2, "w") as f:
            f.write("${val}")
        
        env = { "val" : "replaced" }
        Substitute(tmp_dir, exclude="*.dat").run(env)
        
        with open(tmp_file1) as f:
            self.assertEquals(f.read(), "replaced")
            
        with open(tmp_file2) as f:
            self.assertEquals(f.read(), "${val}")
            
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()