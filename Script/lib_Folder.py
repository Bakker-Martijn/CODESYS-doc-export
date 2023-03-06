#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
from lib_Base import GetChildrenAll, GetPrimaryObject, getName, getType
import Constants
from funcs import list_ExtractColumn

def isFolder(object):
    # type: (any) -> bool

    return object.is_folder

def isDevice(object):
    # type: (any) -> bool

    return object.is_device

def GetAllFolders(object = None, cntDevAsFolder = True, lvl = 0):
    # type: (object, bool, int) -> list[object, str]

    # list[object, name]
    foldersList = GetChildrenAll()

    for object in foldersList:
        if not (isFolder(object[0]) or (cntDevAsFolder and isDevice(object[0]))):
            foldersList.remove(object)
    
    return foldersList