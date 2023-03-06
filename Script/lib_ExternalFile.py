#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
from enum import Enum

#Enums
class ReferenceMode(Enum):
    Link = 0
    LinkAndEmbed = 1
    Embed = 2

class AutoUpdateMode(Enum):
    Always = 0
    Prompt = 1
    Never = 2


def isExternalFile(object):
    # type: (any) -> bool

    return object.is_external_file_object

def createExternalFile(destObject, filePath, name=None, ReferenceMode=ReferenceMode.Embed, AutoUpdate=AutoUpdateMode.Never):
    # type: (any, str, str, ReferenceMode, AutoUpdateMode) -> bool

    if destObject == None:
        raise Exception('No destObject given')
    
    if not Folder.isFolder(destObject):
        raise Exception('destObject is not a folder')

    if filePath == None:
        raise Exception('No filePath given')
    
    if not os.path.isfile(filePath):
        raise Exception('The file cannot be found')
    
    destObject.create_external_file_object(filePath, name, ReferenceMode, AutoUpdate)

    return True

