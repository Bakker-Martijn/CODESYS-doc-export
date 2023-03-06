#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess
from lib_Folder import GetAllFolders, isFolder
from lib_Base import getType, containsObject, getName
from lib_ExternalFile import createExternalFile
from funcs import list_ExtractColumn, saveTxtFile
import Constants




if __name__=='__main__':
    # Get all available folders
    folders = []

    for folder in GetAllFolders():
        if isFolder(folder[0]) and not containsObject(Constants.FolderInfo, folder[0]):
            folders.append((folder[0], "-"*folder[1] + folder[2]))

    if len(folders) < 1:
        system.ui.warning("No folders have been found. (Do all folders already contain a" + Constants.FolderInfo + "file?)")
    else:
        #Let the user choose where to add the folders
        selectedfolder = system.ui.select_many(
            "Select one or more folders you'd like to add a " + Constants.FolderInfo + " file.", 0, 0, list_ExtractColumn(folders, 1))
        
        i = 0
        for item in selectedfolder[1]:
            if item == True:
                path = saveTxtFile(Constants.appdataTmp, "CDS_" + getName(folders[i][0]))
                createExternalFile(folders[i][0], path, Constants.FolderInfo)

            i = i + 1