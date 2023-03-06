#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
from lib_Folder import isFolder


def isExternalFile(object):
    # type: (any) -> bool

    return object.is_external_file_object

def createExternalFile(destObject, filePath, name=None, ReferenceMode = ReferenceMode.Embed, AutoUpdate = AutoUpdateMode.Never):
    # type: (any, str, str, int, int) -> bool

    if destObject == None:
        raise Exception('No destObject given')
    
    if not isFolder(destObject):
        raise Exception('destObject is not a folder')

    if filePath == None:
        raise Exception('No filePath given')
    
    if not os.path.isfile(filePath):
        raise Exception('The file cannot be found')
    
    destObject.create_external_file_object(filePath, name, ReferenceMode, AutoUpdate)

    return True

