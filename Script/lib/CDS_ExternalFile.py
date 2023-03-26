#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
from scriptengine import *


def createExternalFile(destObject, filePath, name=None, ReferenceMode = ReferenceMode.Embed, AutoUpdate = AutoUpdateMode.Never):
    # type: (ScriptExternalFileObjectContainer, str, str, ReferenceMode, AutoUpdateMode) -> bool

    if destObject == None:
        raise Exception('No destObject given')

    if not destObject.may_contain_external_file_objects:
        raise Exception('destObject is not a folder')

    if filePath == None:
        raise Exception('No filePath given')
    
    if not os.path.isfile(filePath):
        raise Exception('The file cannot be found')
    
   
    destObject.create_external_file_object(filePath, name, ReferenceMode, AutoUpdate)

    return True

