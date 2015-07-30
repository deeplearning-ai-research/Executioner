'''
Created on Jul 30, 2015

@author: dhadka
'''

class TaskError(Exception):
    def __init__(self, message):
        super(TaskError, self).__init__(message)
