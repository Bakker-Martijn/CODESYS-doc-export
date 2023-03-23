#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess
from lib.Base import *
from lib.ExternalFile import createExternalFile
from lib.funcs import saveTxtFile, nameof
import Constants
from scriptengine import *


if __name__=='__main__':
    # Get all available folders

    # get all objects
    folders = GetPrimary().get_children(True)                          # type: list[ScriptObject]


    # remove all folders which may not contain an external file (use getattr, 'because not all ScriptObject contain the attribute)
    folders = [x for x in folders if getattr(x, 'may_contain_external_file_objects', False) == True] # type: list[ScriptObject]

    #Remove all folders which already contain an folderInfo file
    folders = [x for x in folders if not len(x.find(Constants.FolderInfo)) > 0] # type: list[ScriptObject]


    if len(folders) < 1:
        system.ui.warning("No folders have been found. \n\n Do all suitable folders already contain a '" + Constants.FolderInfo + "' file?")
    else:
        #Get, and format, all names
        folderNames = [x.get_name(True) for x in folders]

        #Let the user choose where to add the folders
        selectedfolders = system.ui.select_many(
            "Select one or more folders you'd like to add a " + Constants.FolderInfo + " file.", 0, 0, folderNames)
        
        #Get all indexes which are set to TRUE
        indexes = [i for i, val in enumerate(selectedfolders[1]) if val]   
        #add txtFile in every index
        for index in indexes:
            path = saveTxtFile(Constants.appdataTmp, "CDS_" + getName(folders[index]))
            createExternalFile(folders[index], path, Constants.FolderInfo)