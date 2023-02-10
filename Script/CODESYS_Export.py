# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function
import os
import shutil
import time
import subprocess
import re

StartString = """
=============================================================
--- CODESYS Sript, Easily create documentation")
--- Creator: Martijn Bakker")
--- Version: V0.1")
--- See https://github.com/Bakker-Martijn/CODESYS_DocCreation
"""

type_dist={
'792f2eb6-721e-4e64-ba20-bc98351056db':'pm',    #property method
'2db5746d-d284-4425-9f7f-2663a34b0ebc':'dut',   #dut
'adb5cb65-8e1d-4a00-b70a-375ea27582f3':'lib',   #lib manager
'f89f7675-27f1-46b3-8abb-b7da8e774ffd':'m',     #method no ret
'8ac092e5-3128-4e26-9e7e-11016c6684f2':'act',   #action 
'6f9dac99-8de1-4efc-8465-68ac443b7d08':'pou',   #pou
'6654496c-404d-479a-aad2-8551054e5f1e':'itf',   #interface 
'738bea1e-99bb-4f04-90bb-a7a567e74e3a':'',	    #folder
'ffbfa93a-b94d-45fc-a329-229860183b1d':'gvl',   #global var
'5a3b8626-d3e9-4f37-98b5-66420063d91e':'prop',  #property
'2bef0454-1bd3-412a-ac2c-af0f31dbc40f':'tl',    #textlist
'63784cbb-9ba0-45e6-9d69-babf3f040511':'gtl',   #global textlist
'225bfe47-7336-4dbc-9419-4105a7c831fa':'dev',   #device
'ae1de277-a207-4a28-9efb-456c06bd52f3':'tc',    #task configuration
'f8a58466-d7f6-439f-bbb8-d4600e41d099':'m',     #method with ret
'261bd6e6-249c-4232-bb6f-84c2fbeef430':'gvl',   #gvl_Persistent
'98a2708a-9b18-4f31-82ed-a1465b24fa2d':'task',  #task
'40b404f9-e5dc-42c6-907f-c89f4a517386':'Logic'  #Plc Logic
}

ElementList = ['']                                  # Var which contains all pou's, structs e.g. to (used to now if certain type exists in project to make reference)

class Directory():
    def __init__(self, indexHeader, baseDirectry, subDirectory):
        # type: (str, str, str) -> None
        if '\n' in indexHeader:
            self.IndexHeader = indexHeader
        else:
            self.IndexHeader = indexHeader + "\n" + "="*len(indexHeader) + "\n\n"
        self.SubDirectory = subDirectory
        self.Directory = os.path.join(baseDirectry, subDirectory)
        if not os.path.exists(self.Directory):
            os.makedirs(self.Directory)
        self.IndexElements = []

    def AddRstFile(self, Name, str):
        # type: (str, str, bool) -> None
        path = os.path.join(self.Directory, Name)
        with open(path, 'w') as txt:
            txt.write(str)
        self.IndexElements.append(Name)

    def AddIndexElement(self, ElementName):
        # type: (str) -> None
        self.IndexElements.append(ElementName)

    def close(self):
        indexDir = os.path.join(self.Directory, "index.rst")
        with open(indexDir, 'w') as rst:
            if self.SubDirectory != "":
                rst.write(".. _" + self.SubDirectory + ":\n\n")
            rst.write(self.IndexHeader + "\n\n\n")
            rst.write(".. toctree::\n")
            rst.write("   :maxdepth: 1\n")
            rst.write("   :hidden:\n\n")
            for element in self.IndexElements:
                rst.write("   " + element + "\n")

def re_VarClean (str):
    # type: (str) -> str
    str = re.sub(r':', '', str)
    str = re.sub(r'=', '', str)
    str = re.sub(r';', '', str)
    str = re.sub(r',', '', str)
    str = re.sub(r'//', '', str)
    str = re.sub(r'^ ', '', str)
    str = re.sub(r' +', ' ', str)
    str = re.sub(r' +$', '', str)
    str = re.sub(r'\n*', '', str)
    return str

def re_CommentClean (str):
    # type: (str) -> str
    str = re.sub(r':', '', str)
    str = re.sub(r'=', '', str)
    str = re.sub(r';', '', str)
    str = re.sub(r'//', '', str)
    str = re.sub(r'^ ', '', str)
    str = re.sub(r' +', ' ', str)
    str = re.sub(r' +$', '', str)
    str = re.sub(r'\n*', '', str)
    return str

def re_InfoClean (str):
    # type: (str) -> str
    str = re.sub(r'\(\*', '', str)
    str = re.sub(r'\*\)', '', str)
    return str

def re_ContentClean (str):
    # type: (str) -> str
    str = re.sub(r'\t+', ' ', str)
    str = re.sub(r' +', ' ', str)
    str = re.sub(r'\n ', '\n', str)
    str = re.sub(r'\n+', '\n', str)
    str = re.sub(r'^ ', '', str)
    str = re.sub(r'^\n*', '', str)
    return str

def PouParser(Content, Elements):
    # type: (str, list[str]) -> None
    re_InfoPattern = re.compile(r'(\(\*.*?\*\))', flags=re.DOTALL)
    re_SectionPattern = re.compile(r'^VAR.*?(?=END_VAR)', flags=re.DOTALL | re.MULTILINE)
    re_VariablePattern = re.compile(r'(?:^\s*?//).*\n|(?=.*?:)(?:.*?|\n)*;.*(?:\n|)|.*\n')
    re_CommentPattern = re.compile(r'(?:[/])(?:.*?(?:\n|$))')
    re_ValuePattern = re.compile(r'(:=.*?$)', flags=re.DOTALL)
    re_TypePattern = re.compile(r'(:.*?$)', flags=re.DOTALL)

    PouInfo = re_InfoPattern.findall(Content)           #Get info section of pou
    Content = re_ContentClean(Content)                  #First clean content (get rid of \t etc.)
    for var in PouInfo:                                 #Remove info string from content
        Content = Content.replace(var, "")
    PouInfo = ' '.join(PouInfo)
    PouInfo = re_InfoClean(PouInfo)

    PouVariables = ""

    Sections = re_SectionPattern.findall(Content)       #Find all sections in content
    for match in Sections:                              #Loop trough every section

        Variables = re_VariablePattern.findall(match)   #Get all present variables

        Table = Variables[0]                            #First var is always VAR_INPUT or similar
        Table = Table + "~"*len(Variables[0]) + "\n\n"

        # The table for an POU has (always) four columns:
        Column0 = ["Name"]
        Column1 = ["Type"]
        Column2 = ["Value"]
        Column3 = ["Comment"]

        for i in range(1, len(Variables)):              #Loop trough every variable
            #First find the comment
            Comments = re_CommentPattern.findall(Variables[i])
            for var in Comments:
                Variables[i] = Variables[i].replace(var, "")

            #Second find the variable 
            Value = re_ValuePattern.findall(Variables[i])
            for var in Value:
                Variables[i] = Variables[i].replace(var, "")

            #Third find the type
            Type = re_TypePattern.findall(Variables[i])
            for var in Type:
                Variables[i] = Variables[i].replace(var, "")

            #Fourth find the Name
            Name = Variables[i]


            if Value:
                Value = ' '.join(Value)
                Value = re_VarClean(Value)
            else:
                Value = " "

            if Type:     
                Type = ' '.join(Type)   
                Type = re_VarClean(Type)
                if Type in Elements:
                    Type = ':ref:`' + Type + '`'
            else:
                Type = " "

            if Name:           
                Name = re_VarClean(Name)
            else:
                Name = " "

            #Clean up comment
            if Comments:
                Comments = ' '.join(Comments)
                Comments = re_CommentClean(Comments)
            else:
                Comments = " "

            Column0.append(Name)
            Column1.append(Type)
            Column2.append(Value)
            Column3.append(Comments)

        #find the minimum lengt for each column
        Column0Length = max(len(x) for x in Column0) + 2
        Column1Length = max(len(x) for x in Column1) + 2
        Column2Length = max(len(x) for x in Column2) + 2
        Column3Length = max(len(x) for x in Column3) + 2

        #first create headers
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "  " + "="*Column3Length + "\n"
        Table = Table + Column0[0] + " "*(Column0Length - len(Column0[0]) + 2)
        Table = Table + Column1[0] + " "*(Column1Length - len(Column1[0]) + 2)
        Table = Table + Column2[0] + " "*(Column2Length - len(Column2[0]) + 2)
        Table = Table + Column3[0] + " "*(Column3Length - len(Column3[0]) + 2) + "\n"
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "  " + "="*Column3Length + "\n"

        # Loop through all lines
        for i in range(1, len(Column0)):
            if Column0[i] == " ":
                Table = Table + Column3[i] + "\n"
                Table = Table + "-"*(Column0Length + Column1Length + Column2Length + Column3Length + 6) + "\n"
            else:
                Table = Table + Column0[i] + " "*(Column0Length - len(Column0[i]) + 2)
                Table = Table + Column1[i] + " "*(Column1Length - len(Column1[i]) + 2)
                Table = Table + Column2[i] + " "*(Column2Length - len(Column2[i]) + 2)
                Table = Table + Column3[i] + " "*(Column3Length - len(Column3[i]) + 2) + "\n"

        # Add table end
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "  " + "="*Column3Length + "\n\n"

        PouVariables = PouVariables + Table

    return PouInfo + "\n\n" + PouVariables

def DutParser(Content, Elements):
    # type: (str, list[str]) -> None
    #There are two types of duts: STRUCT or ENUM
    re_InfoPattern = re.compile(r'(\(\*.*?\*\))', flags=re.DOTALL)
    if 'STRUCT' in Content:
        re_SectionPattern = re.compile(r'(?<=STRUCT\n).*?(?=END_STRUCT)', flags=re.DOTALL)
        re_VariablePattern = re.compile(r'(?=^//).*\n|(?=.*?:)(?:.*?|\n)*;.*(?:\n|)|.*\n')
    else:
        re_SectionPattern = re.compile(r'(?<=\().*?(?=\))', flags=re.DOTALL)
        re_VariablePattern = re.compile(r'(?=^//).*\n|(?=.*?:)(?:.*?|\n)*(?:,|$).*')
    
    re_CommentPattern = re.compile(r'(?:[/])(?:.*?(?:\n|$))')     
    re_TypePattern = re.compile(r'(:.*?$)', flags=re.DOTALL)

    PouInfo = re_InfoPattern.findall(Content)           #Get info section of pou
    Content = re_ContentClean(Content)                  #First clean content (get rid of \t etc.)
    for var in PouInfo:                                 #Remove info string from content
        Content = Content.replace(var, "")
    PouInfo = ' '.join(PouInfo)
    PouInfo = re_InfoClean(PouInfo)

    PouVariables = ""

    Sections = re_SectionPattern.findall(Content)       #Find all sections in content
    for match in Sections:                              #Loop trough every section

        Variables = re_VariablePattern.findall(match)   #Get all present variables

        if 'STRUCT' in Content:
            Table = "STRUCT\n"
            Column0 = ["Name"]
            Column1 = ["Type"]
            Column2 = ["Comment"]
        else:
            Table = "ENUM\n"
            Column0 = ["Name"]
            Column1 = ["Value"]
            Column2 = ["Comment"]

        Table = Table + "~~~~~~~~~~~~~~~~~~~~\n\n"

        for i in range(0, len(Variables)):              #Loop trough every variable
            #First find the comment
            Comments = re_CommentPattern.findall(Variables[i])
            for var in Comments:
                Variables[i] = Variables[i].replace(var, "")

            #Second find the type
            Type = re_TypePattern.findall(Variables[i])
            for var in Type:
                Variables[i] = Variables[i].replace(var, "")
                if 'STRUCT' in Content:
                    if Type in Elements:
                        Type = ':ref:`' + Type + '`'

            #Third find the Name
            Name = Variables[i]

            if Type:     
                Type = ' '.join(Type)   
                Type = re_VarClean(Type)
            else:
                Type = " "

            if Name:           
                Name = re_VarClean(Name)
            else:
                Name = " "

            #Clean up comment
            if Comments:
                Comments = ' '.join(Comments)
                Comments = re_CommentClean(Comments)
            else:
                Comments = " "

            Column0.append(Name)
            Column1.append(Type)
            Column2.append(Comments)

        #find the minimum lengt for each column
        Column0Length = max(len(x) for x in Column0) + 2
        Column1Length = max(len(x) for x in Column1) + 2
        Column2Length = max(len(x) for x in Column2) + 2

        #first create headers
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "\n"
        Table = Table + Column0[0] + " "*(Column0Length - len(Column0[0]) + 2)
        Table = Table + Column1[0] + " "*(Column1Length - len(Column1[0]) + 2)
        Table = Table + Column2[0] + " "*(Column2Length - len(Column2[0]) + 2) + "\n"
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "\n"

        # Loop through all lines
        for i in range(1, len(Column0)):
            if Column0[i] == " ":
                Table = Table + Column2[i] + "\n"
                Table = Table + "-"*(Column0Length + Column1Length + Column2Length + 4) + "\n"
            else:
                Table = Table + Column0[i] + " "*(Column0Length - len(Column0[i]) + 2)
                Table = Table + Column1[i] + " "*(Column1Length - len(Column1[i]) + 2)
                Table = Table + Column2[i] + " "*(Column2Length - len(Column2[i]) + 2) + "\n"

        # Add table end
        Table = Table + "="*Column0Length + "  " + "="*Column1Length + "  " + "="*Column2Length + "\n\n"

        PouVariables = PouVariables + Table

    return PouInfo + "\n\n" + PouVariables

def TextualDeclaration_Parser(treeobj, header = ""):
    # type: (Any, str) -> None
    Type = type_dist[treeobj.type.ToString()]               #Save type string
    Name = str(treeobj.get_name())                        #get the folder name

    Content = ""

    if Type == "dut":
        Content = DutParser(treeobj.textual_declaration.text, ElementList)
    elif Type == "pou":
        Content = PouParser(treeobj.textual_declaration.text, ElementList)
    elif Type == "gvl":
        Content = PouParser(treeobj.textual_declaration.text, ElementList)
    else:
        Content = "UNKNOWN, couldn't parse information"

    if header == "":
        return ".. _" + Name + ":\n\n" + Name + " (" + Type + ")\n" + "="*(len(Name) + len(Type) + 3) + "\n\n" + Content
    else:
        return ".. _" + header + ":\n\n" + Name + " (" + Type + ")\n" + "="*(len(Name) + len(Type) + 3) + "\n\n" + Content

def Save_POUS(treeobj, dir):
    # type: (Any, Directory) -> None
    Name = treeobj.get_name()  	                        #Get object name/header

    if Name[0] == '_':
        return

    if treeobj.is_folder:                               # object is a folder
        dir.AddIndexElement(Name + "//index")
        curDir = Directory(Name, dir.Directory, Name)      

        for child in treeobj.get_children(False):
            Save_POUS(child, curDir)                      # iterate trough all child elements of the folder

    elif Name == "FolderInfo":                          # Object is a folderInfo (containing info about the folder)
        dir.IndexHeader = bytearray(treeobj.get_data()).decode().replace('\r', '')

    elif treeobj.type.ToString() in type_dist:
        if treeobj.has_textual_declaration:
            if re.search('__EXCLUDE__', treeobj.textual_declaration.text, re.MULTILINE):
                return

            dir.AddRstFile(Name + '.rst', TextualDeclaration_Parser(treeobj))
    
    dir.close()

def Save_Devices(treeobj, dir):
    # type: (Any, Directory) -> None

    if treeobj.is_device:
        appName = treeobj.get_name() 
        DeviceDir = Directory(appName, dir.Directory, appName)

        dir.AddIndexElement(appName + "//index")

        DeviceStr = 'Devices\n=======\n\nCPU I/O Devices:\n'

        for child in treeobj.get_children(False):
            if HasDeviceChild(child):
                DeviceStr = DeviceStr + Append_Devices(child)
            elif child.get_name() == "FolderInfo":                          # Object is a folderInfo (containing info about the folder)
                DeviceDir.IndexHeader = bytearray(child.get_data()).decode().replace('\r', '')
            
            append_DevicePous(child, DeviceDir)

        DeviceDir.AddRstFile('Devices.rst', DeviceStr)

        DeviceDir.close()
            
    dir.close()

def Append_Devices(TreeObj, depth = 0):
    # type: (any, int) -> str
    string = ""

    if depth == 0:
        string = string + '\n- \'' + TreeObj.get_name() + '\'\n\n'
        for child in  TreeObj.get_children(False):
            if HasDeviceChild(child):
                string = string + Append_Devices(child, depth + 1)
    else:
        string = string + '   '*depth + '\'' + TreeObj.get_name() + '\'\n\n'
        for child in  TreeObj.get_children(False):
            if HasDeviceChild(child):
                string = string + Append_Devices(child, depth + 1)
    
    return string

def HasDeviceChild(TreeObj):
    # type: (any) -> bool

    if TreeObj.is_device:
        return True

    HasDevice = False

    for child in  TreeObj.get_children(False):
        if child.is_device:
            HasDevice = True
            break

    return HasDevice

def append_DevicePous(treeObj, dir):
        # type: (any, Directory) -> None

        name = dir.SubDirectory + treeObj.get_name()

        if treeObj.type.ToString() in type_dist:
            if treeObj.has_textual_declaration:
                if re.search('__EXCLUDE__', treeObj.textual_declaration.text, re.MULTILINE):
                    return

                dir.AddRstFile(name + '.rst', TextualDeclaration_Parser(treeObj, name))

        for child in  treeObj.get_children(False):
            append_DevicePous(child, dir)

def PopulateElementList(treeObj):

    if treeObj.is_device:
        return

    elements = treeObj.get_children(False)

    if len(elements) > 0:
        for element in elements:
            PopulateElementList(element)
    else:
        ElementList.append(treeObj.get_name(False))

print(StartString)

Dir = system.ui.browse_directory_dialog("Choose a directory where the parsed files will be stored")
if Dir is None:
    print ("No selection made, no files were created.")
    System.exit()
else:
    print("Saving the parsed files in: '%s'" % Dir)

Dir_Home = Directory('CODESYS Project', Dir, "")
Dir_Home.AddIndexElement('Pous//index')
Dir_Home.AddIndexElement('Devices//index')
Dir_Pou = Directory('Pous', Dir_Home.Directory, 'Pous')
Dir_Devices = Directory('Devices', Dir_Home.Directory, 'Devices')

proj = projects.primary
for child in proj.get_children(False):
    # Create poject tree, to see what is present in the project
    PopulateElementList(child)      

    # If an static directory is found (startis with '_', then all the files will be copied straight into the output)
    if child.get_name()[0] == '_':
        Dir_Static = Directory("", Dir_Home.Directory, child.get_name())

        for file in child.get_children(False):
            file.get_data(os.path.join(Dir_Static.Directory, file.get_name(False)))


for child in proj.get_children(False):
    Save_POUS(child, Dir_Pou)

for child in proj.get_children(False):
    Save_Devices(child, Dir_Devices)

ProjInfotxt = proj.find("ProjectInfo", True)
if len(ProjInfotxt) > 0:
    ProjInfotxt = ProjInfotxt[0]
    Dir_Home.IndexHeader = bytearray(ProjInfotxt.get_data()).decode().replace('\r', '')

PousInfotxt = proj.find("PousInfo", True)
if len(PousInfotxt) > 0:
    PousInfotxt = PousInfotxt[0]
    Dir_Pou.IndexHeader = bytearray(PousInfotxt.get_data()).decode().replace('\r', '')

DevicesInfotxt = proj.find("DevicesInfo", True)
if len(DevicesInfotxt) > 0:
    DevicesInfotxt = DevicesInfotxt[0]
    Dir_Devices.IndexHeader = bytearray(DevicesInfotxt.get_data()).decode().replace('\r', '')

Dir_Home.close()
Dir_Pou.close()
Dir_Devices.close()
print("--- Script finished. ---")