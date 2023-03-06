#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess
from lib_Folder import GetAllFolders
from lib_Base import getType, containsObject
from funcs import list_ExtractColumn
import Constants

AcceptedFolderTypes = ["fldr", "app", "dev"]


if __name__=='__main__':
    # Get all available folders
    folders = []

    for folder in GetAllFolders():
        if getType(folder[0]) in AcceptedFolderTypes and not containsObject(Constants.FolderInfo, folder[0]):
            folders.append((folder[0], "-"*folder[1] + folder[2]))
    
    print(folders)


    if len(folders) < 1:
        system.ui.warning("No folders have been found. (Do all folders already contain a" + Constants.FolderInfo + "file?)")

    #Let the user choose where to add the folders
    selectedfolder = system.ui.select_many(
        "Select one or more folders you'd like to add a " + Constants.FolderInfo + " file.", 0, 0, list_ExtractColumn(folders, 1))



    print("The user selected option '%s'" % str(selectedfolder)) # res is a tuple