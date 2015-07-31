'''
Created on Jul 30, 2015

@author: dhadka
'''
import os
import logging
import subprocess
import shlex
import utils
import tempfile
from exceptions import TaskError
from threading import Thread

class Task(object):
    '''
    Generic tasks, subclasses must override run(env).
    '''
    
    def __init__(self):
        super(Task, self).__init__()
        
    def run(self, env):
        raise NotImplementedError("Tasks must define the run method")
    
    
class CreateTempDir(Task):
    '''
    Creates a new, empty temporary directory and sets WORK_DIR to this
    temporary directory.
    '''
    
    def __init__(self):
        super(CreateTempDir, self).__init__()
        
    def run(self, env):
        logging.info("Creating temporary directory")
        dir = tempfile.mkdtemp()
        env["WORK_DIR"] = dir
        logging.info("Successfully created temporary directory: " + dir)
        
        
class DeleteTempDir(Task):
    '''
    Deletes the temporary directory created by CreateTempDir.
    '''
    
    def __init__(self):
        super(DeleteTempDir, self).__init__()
        
    def run(self, env):
        if not "WORK_DIR" in env:
            logging.error("WORK_DIR not defined")
            raise TaskError("WORK_DIR not defined")
        
        dir = env["WORK_DIR"]
        logging.info("Deleting temporary directory: " + dir)
        utils.remove(dir)
        logging.info("Successfully deleted temporary directory")
        
        
class SetWorkDir(Task):
    '''
    Sets the WORK_DIR.
    '''
    
    def __init__(self, dir):
        super(SetWorkDir, self).__init__()
        self.dir = dir
        
    def run(self, env):
        logging.info("Setting work directory")
        env["WORK_DIR"] = self.dir
        logging.info("Successfully set work directory: " + self.dir)   
        
        
class Delete(Task):
    '''
    Deletes a file or directory.
    '''
    
    def __init__(self, path):
        super(Delete, self).__init__()
        self.path = path
        
    def run(self, env):
        logging.info("Deleting " + str(self.path))
        
        if type(self.path) is list or type(self.path) is tuple:
            for p in self.path:
                utils.remove(p)
        else:
            utils.remove(self.path)
        
        
class Copy(Task):
    '''
    Copies the contents of the given folder to WORK_DIR.
    '''
    
    def __init__(self, fromDir, toDir=None):
        super(Copy, self).__init__()
        self.fromDir = fromDir
        self.toDir = toDir
        
    def run(self, env):
        toDir = self.toDir
        
        if toDir is None:
            if not "WORK_DIR" in env:
                logging.error("WORK_DIR not defined")
                raise TaskError("WORK_DIR not defined")
            toDir = env["WORK_DIR"]
        
        logging.info("Copying " + self.fromDir + " to " + toDir)
        utils.copytree(self.fromDir, toDir)
        logging.info("Successfully copied folder contents")
        

class Substitute(Task):
    '''
    Substitutes ${keyword} fields in all files with their assigned values.
    '''
    
    def __init__(self, folder=None):
        super(Substitute, self).__init__()
        self.folder = folder
        
    def run(self, env):
        folder = self.folder
        
        if folder is None:
            if not "WORK_DIR" in env:
                logging.error("WORK_DIR not defined")
                raise TaskError("WORK_DIR not defined")
            folder = env["WORK_DIR"]
            
        logging.info("Substituting keywords in " + dir)
        utils.substitutetree(dir, env)
        logging.info("Successfully substituted keywords")
        
        
class Execute(Task):
    '''
    Executes a program.
    '''
    
    def __init__(self, command, timeout=None):
        super(Execute, self).__init__()
        self.command = command
        self.timeout = timeout
        
    def run(self, env):
        command = utils.substitute(self.command, env)
        
        logging.info("Executing command " + command)
        process = subprocess.Popen(shlex.split(command),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        env["PROCESS"] = process
        env["STDIN"] = process.stdin
        env["STDOUT"] = process.stdout
        env["STDERR"] = process.stderr
        
        Thread(target=utils.process_monitor, args=(process,), kwargs={ "timeout":self.timeout }).start()

        logging.info("Successfully executed command")
        

class CheckExitCode(Task):
    '''
    Checks the exit code after running Execute.
    '''
    
    def __init__(self, ok=0):
        super(CheckExitCode, self).__init__()
        
        if type(ok) is not list:
            self.ok = [ ok ]
        else:
            self.ok = ok
        
    def run(self, env):
        if "PROCESS" not in env:
            logging.error("PROCESS not set, call Execute before CheckExitCode")
            raise TaskError("PROCESS not set, call Execute before CheckExitCode")
        
        env["EXIT_CODE"] = env["PROCESS"].wait()
        
        if env["EXIT_CODE"] not in self.ok:
            logging.error("Execute failed, expected exit code " + str(self.ok) + ", received " + str(env["EXIT_CODE"]))
            raise TaskError("Execute failed, expected exit code " + str(self.ok) + ", received " + str(env["EXIT_CODE"]))
        
        logging.info("Exit code ok")
        
        
class WriteInput(Task):
    '''
    Writes to the STDIN of the running process.
    '''
    
    def __init__(self, input):
        super(WriteInput, self).__init__()
        self.input = input
        
    def run(self, env):
        if "STDIN" not in env:
            logging.error("STDIN not defined, run Execute first")
            raise TaskError("STDIN not defined, run Execute first")
        
        formatted_input = utils.substitute(self.input, env)
        
        logging.info("Sending input to stdin: " + formatted_input)
        stdin = env["STDIN"]
        stdin.write(formatted_input)
        stdin.flush()
        
    
        
class PrintEnv(Task):
    '''
    Prints the environment variables.
    '''
    
    def __init__(self):
        super(PrintEnv, self).__init__()
        
    def run(self, env):
        print(env)
        
        
class WriteFile(Task):
    '''
    Writes the contents of a file.
    '''
    
    def __init__(self, file, content):
        super(WriteFile, self).__init__()
        self.file = file
        self.content = content
        
    def run(self, env):
        folder = env["WORK_DIR"]
        absfile = os.path.join(folder, self.file)
        
        logging.info("Creating file " + str(absfile))
        
        with open(absfile, 'w') as file:
            file.write(utils.substitute(self.content, env))
        
        logging.info("Successfully created file")
        

class ParseOutput(Task):
    '''
    Parses the output from the last Execute call.
    '''
    
    def __init__(self, callback):
        super(ParseOutput, self).__init__()
        self.callback = callback
        
    def run(self, env):
        results = self.callback(env["STDOUT"])
        env.update(results)


class ParseLine(Task):
    '''
    Parses a line from the last Execute call.
    '''
    
    def __init__(self, name="output", delimiters=None, type=str):
        super(ParseLine, self).__init__()
        self.name = name
        self.delimiters = delimiters
        self.type = type
        
    def run(self, env):
        stdout = env["STDOUT"]
        line = stdout.readline()
        
        logging.info("Parsed line " + line)
        values = map(self.type, line.split(self.delimiters))
        
        if type(self.name) is list:
            if len(self.name) != len(values):
                logging.error("Number of parsed values (" + str(len(values)) + ") does not match number of names (" + str(len(self.name)) + ")")
                raise TaskError("Number of parsed values (" + str(len(values)) + ") does not match number of names (" + str(len(self.name)) + ")")
            
            for i, name in enumerate(self.name):
                env.update({ name : values[i] })
        else: 
            env.update({ self.name : values })
        
        
        
class Format(Task):
    '''
    Formats a field.
    '''
    
    def __init__(self, name, format="{}", rename=None):
        super(Format, self).__init__()
        self.name = name
        self.format = format
        self.rename = rename
        
    def run(self, env):
        if self.name not in env:
            logging.error(self.name + " is not set in environment")
            raise TaskError(self.name + " is not set in environment")
        
        new_name = self.rename
        if new_name is None:
            new_name = self.name
        
        logging.info("Formatting " + self.name)
        old_val = env[self.name]
        
        if callable(self.format):
            env[new_name] = self.format(old_val)
        else:
            env[new_name] = self.format.format(old_val)
            
        logging.info("Saved " + new_name + " as " + str(env[new_name]))
        

class Return(Task):
    '''
    Picks a subset of the fields to return.
    '''
    
    def __init__(self, *fields):
        super(Return, self).__init__()
        self.fields = fields
        
    def run(self, env):
        unwanted = set(env.keys()) - set(self.fields)
        
        for key in unwanted:
            del env[key]
