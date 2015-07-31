'''
Created on Jul 30, 2015

@author: dhadka
'''

import os
import re
import shutil
import time
import logging
from string import Template

def copytree(src, dst):
    '''
    Similar to shutil.copytree, except it works even when the dst folder exists.
    '''
    
    if not os.path.exists(dst):
        os.makedirs(dst)
        
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isdir(s):
            copytree(s, d)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
                
def get_substitution_key(str, env):
    substitionEngine = SubstitionEngine(str)
    
    if (substitionEngine.is_substitution_str()):
        if substitionEngine.get_substitution_name() in env:
            return substitionEngine.get_substitution_name()
        else:
            return None
    else:
        return None
                
def substitute(str, env):
    substitionEngine = SubstitionEngine(str)
    return substitionEngine.substitute(env)

def substitutetree(src, env):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        
        if os.path.isdir(s):
            substitutetree(s, env)
        else:
            with open(s) as file:
                substitionEngine = SubstitionEngine(file.read())
                
            with open(s, 'w') as file:
                file.write(substitionEngine.substitute(env))
                
def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
        
def process_monitor(process, timeout=None):
    start = time.time()
    
    while True:
        if process.poll() is None:
            if timeout is not None and time.time() - start > timeout:
                logging.warn("Process exceeded timeout limit, killing process")
                process.kill()
            
            time.sleep(1)
        else:
            break
        
    logging.info("Process terminated with exit code " + str(process.returncode))
                
def redirect(stream, env, name):
    while True:
        line = stream.readline()
        
        if not line:
            break

        env[name].seek(0, os.SEEK_END)
        env[name].write(line)
        print(env[name].getvalue())
        
# Copied from Lib/string.py
class _multimap:
    """Helper class for combining multiple mappings.
    Used by .{safe_,}substitute() to combine the mapping and keyword
    arguments.
    """

    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]
        
class SubstitionEngine(object):
    
    def __init__(self, template):
        super(SubstitionEngine, self).__init__()
        self.template = template
        
        self.delimiter = '$'
        self.idpattern = r'[_a-z][_a-z0-9]*'
        
        match_pattern = r"""
            ^%(delim)s(?:
            (?P<escaped>%(delim)s)$ |   # Escape sequence of two delimiters
            (?P<named>%(id)s)$      |   # delimiter and a Python identifier
            {(?P<braced>%(id)s)}$   |   # delimiter and a braced identifier
            (?P<invalid>))$             # Other ill-formed delimiter exprs
            """
        
        sub_pattern = r"""
            %(delim)s(?:
            (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
            (?P<named>%(id)s)      |   # delimiter and a Python identifier
            {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier
            (?P<invalid>))             # Other ill-formed delimiter exprs
            """
            
        self.match_regex = re.compile(match_pattern % {"delim":re.escape(self.delimiter), "id":self.idpattern},
                                 re.IGNORECASE | re.VERBOSE)
        
        self.sub_regex = re.compile(sub_pattern % {"delim":re.escape(self.delimiter), "id":self.idpattern},
                               re.IGNORECASE | re.VERBOSE)
    
    def is_substitution_str(self):       
        return self.match_regex.match(self.template) is not None
    
    def get_substitution_name(self):
        mo = self.match_regex.match(self.template)
        
        if mo is None:
            return None
        
        named = mo.group('named') or mo.group('braced')

        if named is not None:
            return named
        if mo.group('escaped') is not None:
            return self.delimiter
        if mo.group('invalid') is not None:
            return mo.group()

        raise ValueError('Unrecognized named group in pattern',
                          self.pattern)
        
    def has_substitutions(self):
        return self.sub_regex.search(self.template) is not None
    
    # Derived from safe_substitute in Lib/string.py
    def substitute(self, *args, **kws):
        if not args:
            raise TypeError("descriptor 'substitute' of 'Template' object "
                            "needs an argument")

        if len(args) > 1:
            raise TypeError('Too many positional arguments')

        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        # Helper function for .sub()
        def convert(mo):
            named = mo.group('named') or mo.group('braced')

            if named is not None:
                try:
                    # We use this idiom instead of str() because the latter
                    # will fail if val is a Unicode containing non-ASCII
                    return '%s' % (mapping[named],)
                except KeyError:
                    return mo.group()

            if mo.group('escaped') is not None:
                return self.delimiter

            if mo.group('invalid') is not None:
                return mo.group()

            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)

        return self.sub_regex.sub(convert, self.template)