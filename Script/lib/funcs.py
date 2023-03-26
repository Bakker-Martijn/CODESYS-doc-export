#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess

def list_ExtractColumn(list = [], column = 0):
    # type: (list, int) -> list

    if not len(list) > 0:
        raise Exception('empty list given')
    
    return [item[column] for item in list]

def saveTxtFile(Path, name, str = "Auto generated text file", ext = ".txt"):
    # type: (str, str, str, str) -> str

    if Path == None or "":
        raise ValueError("No path given")
    
    if not os.path.exists(Path):
        raise Exception("Given path doesn't exist")
    
    if name == None or "":
        raise Exception("No name given")
    
    path = os.path.join(Path, name + ext)
    with open(path, 'w') as txt:
        txt.write(str)

    return path

