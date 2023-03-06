#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import * #If codesys must import this module, this has to be here
import os, subprocess
import Constants
from funcs import list_ExtractColumn

def GetPrimaryObject():
    # type: () -> object

    return projects.primary

def GetChildren(object, recursive = False):
    # type: (object, bool) -> list[str]

    return object.get_children(recursive)

def GetChildrenAll(object = None, lvl = 0):
    # type: (object, int) -> list[object, int, str]

    # list[object, level, name]
    objectList = []

    if object == None:
        for child in GetChildren(GetPrimaryObject()):
            objectList.extend(GetChildrenAll(child))
    else:
        objectList.append((object, lvl, getName(object)))
        for child in GetChildren(object):
            objectList.extend(GetChildrenAll(child, lvl + 1))

    return objectList


def FindObject(name, startObject = None, recursive = True):
    # type: (str, object, bool) -> object

    if name == None:
        raise Exception('No search string given')
    
    if startObject == None:
        return GetPrimaryObject.find(name, recursive)
    else:
        return startObject.find(name, recursive)

def containsObject(name, startObject = None, recursive = True):
    # type: (str, object, bool) -> bool

    if name == None:
        raise Exception('No search string given')
    
    if len(FindObject(name, startObject, recursive)) > 0:
       return True
    
    return False 

def getName(object, GetLocalName = False):
    # type: (object, bool) -> str
    return object.get_name(GetLocalName)

def isTypeKnown(object):
    # type: (object) -> bool

    return object.type.ToString() in Constants.type_dist

def getType(object):
    # type(object) -> str

    if not isTypeKnown(object):
        return None
    
    return Constants.type_dist[object.type.ToString()]
