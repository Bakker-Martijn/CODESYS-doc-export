#Codesys iron python / python 2.7
from __future__ import print_function
from scriptengine import *

import os, subprocess
import sys
import Constants
import lib.CDS_Consts
from lib.CDS_ExternalFile import createExternalFile
from lib.funcs import saveTxtFile


if __name__=='__main__':
    # Get all available folders

    # list with exceptions, to keep track of occured exception and to show to users
    Exceptions = []                                                                                                 # type: list[(Exception, str)]

    # remove all folders which may not contain an external file 
    # use getattr, 'because not all ScriptObjects contain this attribute
    folders = [x for x in lib.CDS_Consts.ObjectsAll if getattr(x, 'may_contain_external_file_objects', False) == True]             # type: list[ScriptObject]

    #Remove all folders which already contain an folderInfo file
    folders = [x for x in folders if not len(x.find(Constants.FolderInfo)) > 0]                                     # type: list[ScriptObject]

    if len(folders) < 1:
        # there are no files where an txt file may be added
        lib.CDS_Consts.ui.warning(
            "No folders have been found.\n\nDo all folders already contain a " + Constants.FolderInfo + " file?")
        sys.exit()

    #Get, and format, all names
    folderNames = [x.get_name(True) for x in folders]

    #Let the user choose where to add the folders
    result = lib.CDS_Consts.ui.select_many(                                                                            
        "Select one or more folders you'd like to add a " + Constants.FolderInfo + " file to",
        PromptChoice.OKCancel, PromptResult(), folderNames)                                                         # type: list
    
    if result[0] != PromptResult.OK:
        # user has cancelled the action
        sys.exit()
    
    #Get all indexes which are set to TRUE
    indexes = [i for i, val in enumerate(result[1]) if val]  

    if len(indexes) < 1:
        # no files have been chosen
        sys.exit()

    #add txtFile in every index that is in fact true
    for index in indexes:
        #1. create textfile (name should be different for each object, therefore basing names on guid)
        try:
            path = saveTxtFile(Constants.appdataTmp, "CDS_" + str(folders[index].guid))
        except ValueError as e:
            # an error occured, save exception for later communication to user
            Exceptions.extend((e, folders[index].get_name()))
            # move to next index
            continue

        #2. create/upload txt file in CDS
        try:
            createExternalFile(folders[index], path, Constants.FolderInfo)
        except ValueError as e:
            # an error occured, save exception for later communication to user
            Exceptions.extend((e, folders[index].get_name()))

        #3. Remove txt file from filesystem
        os.remove(path)

    if len(Exceptions) > 0:
        # there have been errors during the execution of this script, communicate this to the the user
        lib.CDS_Consts.ui.error(
            "Errors occured during the generation of " + Constants.FolderInfo + " files. One or more " + Constants.FolderInfo + " files may not have been generated.\n\nSee messages tab for error messages.") 
        print(Exceptions)