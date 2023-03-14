#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess
from lib_Base import getName, containsObject, GetChildrenAll
from lib_ExternalFile import createExternalFile, mayContainExternalFile
from funcs import saveTxtFile
import Constants


if __name__=='__main__':
    # Get all available folders
    folders = [x for x in GetChildrenAll() if mayContainExternalFile(x[0])]
    #Remove all folders which already contain an folderInfo file
    folders[:] = [x for x in folders if not containsObject(Constants.FolderInfo, x[0], False)]


    if len(folders) < 1:
        system.ui.warning("No folders have been found. \n\n Do all suitable folders already contain a '" + Constants.FolderInfo + "' file?")
    else:
        #Get, and format, all names
        folderNames = ["-"*x[1] + x[2] for x in folders]

        #Let the user choose where to add the folders
        selectedfolders = system.ui.select_many(
            "Select one or more folders you'd like to add a " + Constants.FolderInfo + " file.", 0, 0, folderNames)
        
        #Get all indexes which are set to TRUE
        indexes = [i for i, val in enumerate(selectedfolders[1]) if val]   
        #add txtFile in every index
        for index in indexes:
            path = saveTxtFile(Constants.appdataTmp, "CDS_" + getName(folders[index][0]))
            createExternalFile(folders[index][0], path, Constants.FolderInfo)