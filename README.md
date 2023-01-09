# CODESYS-doc-export
V1.0  
Creator: M. Bakker

Easily parse CODESYS project into a Spinx Source structure.

# What does the script do?
The script can be ran from the CODESYS ide. And will parse all Pou's, structs etc. in to a folder structure. 

## Sample DOCS
To see how generated documentation (can) look: [Sample documentation](https://codesys-sample-docs.readthedocs.io/en/latest/index.html)

## How does it work?
### 1. CodeSys project:
Create a CODESYS project, describe the variables etc. correctly(!)  
See the [Sample documentation](https://codesys-sample-docs.readthedocs.io/en/latest/index.html) page for tips on how to create documentation  

![CODESYS Project](README_PICS/CODESYS_Project.png?)

### 2. Exported Files:
Run the CODESYS_Export.py script.  
The folders will be saved in a directory of choice. 

![Exported files](README_PICS/Exported_Files.png?)

### Documentation:
Generate documentation using [Sphinx](https://www.sphinx-doc.org/en/master/)  

![Exported files](README_PICS/WebPage.png?)

# Setting up:
See the [Setting up](Setting_Up/SETTING_UP.md) page for info on how to setup and host your documentation on: [ReadTheDocs](https://readthedocs.org/).
