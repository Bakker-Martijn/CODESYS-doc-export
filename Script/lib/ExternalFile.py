#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
from .Base import *

def isExternalFile(object):
    # type: (ScriptObject) -> bool

    object

    try:
        return object.is_external_file_object
    except AttributeError:
        return False

def mayContainExternalFile(object):
    # type: (object) -> bool

    try:
        return object.may_contain_external_file_objects
    except AttributeError:
        print(getName(object))
        return False

def createExternalFile(destObject, filePath, name=None, ReferenceMode = ReferenceMode.Embed, AutoUpdate = AutoUpdateMode.Never):
    # type: (any, str, str, int, int) -> bool

    if destObject == None:
        raise Exception('No destObject given')
    
    if not mayContainExternalFile(destObject):
        raise Exception('destObject is not a folder')

    if filePath == None:
        raise Exception('No filePath given')
    
    if not os.path.isfile(filePath):
        raise Exception('The file cannot be found')
    
    destObject.create_external_file_object(filePath, name, ReferenceMode, AutoUpdate)

    return True

