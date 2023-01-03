# Setting up
## prerequisite
- Make sure Python is installed on the machine (https://Python.org/downloads)
- Make sure GIT is installed on the machine (https://gitforwindows.org)

# Steps
1. Create a (public) repository on github (https://Github.org)
2. Clone the repo on your local machine
   - Create directory on local machine (in here the repo will be stored)
   - Open the Command Prompt
   - Move to the (newly) created folder in CMD (CMD `cd C:Users\DirLocation`)
   - Copy repo HTTPS link (for example)
   ![CODESYS Project](PICS/Clone_Repo_Get_Link.png?)
   - Clone the repo (CMD `git clone https://github.com/Bakker-Martijn/CODESYS-doc-export.git`)
3. The contents of the repo (only README.MD) should be copied into the directory on your local machine
4. Create a python environment `python -m virtualenv env`
5. Activate the environment `env\sripts\activate.bat`
![CODESYS Project](PICS/Activated_env.png?)
(check if activation was succesfull, environment name should be in brackets!)
6. Create new directory in repo (CMD `mkdir docs`)
7. Open the directory (CMD `cd docs`)
8. Install sphinx: (CMD `pip install sphinx==5.3.0`)  
*(version 5.3.0 is mandatory, ReadTheDocs doesn't yet support the newest version)*
9. Run the export script in CODESYS  
![CODESYS Project](PICS/Run_Script.png?)
10. Choose a directory in which the files will be saved
11. Copy the exported files  
![Exported files](PICS/Exported_Files.png?)
12. Paste the files in: Repo/Location/docs/source
![Exported files](PICS/Pasting_Files.png?)
13. Make the html page('s) (CMD `Make html`)
14. Open the created HTML page('s) in: Repo/Location/docs/build/html/genindex.html. 
![Exported files](PICS/Basic_Html_page.png?)  
A page like this should have generated
15. Make any chages you'd like to html page, for more info on how to generate Sphinx documentation using sphinx i higly recommend watching: [How to document with Sphinx tutorial](https://www.youtube.com/playlist?list=PLE72UCmIe7T9HewaqCUhKqiMK3LxYStjy).  
*When created a new page run the `Make html` command again!*
![Exported files](PICS/WebPage.png?) New designed webpage (using the [Picollo_theme](https://github.com/piccolo-orm/piccolo_theme))
16. add requirements.txt  
*used by readtheDocs to find out what packages are used!*
    - (CMD `pip freeze > requirements.txt`)
    - (CMD `pip install -r requirements.txt`)
17. Push the files to github
    - Move to the home of the repo (CMD `CD ..`)
    - Create a .gitIgnore file (CMD `touch .gitignore`)
    - Open the .gitIngore file (in  RepoLocation/.gitIgnore.txt)
       - We want to ingore:   
       Env/ (*the python environment, only works on the local machine*)  
       docs/build/ (*the html output, not necessary for readTheDocs, the site will recreate the output itself*)  
       ![Exported files](PICS/GitIgnore.png?) 
    - Check what the status of the files are (CMD `git status`)
    ![Exported files](PICS/Git_status.png?) 
    should look something like the above picture
    - add the files to be uploaded to github (CMD `git add .`)
    - Commit the files to be uploaded: (CMD `git commit -m "A comment"`)
    - push the files to github (CMD `git push origin main`)
    ![Exported files](PICS/Github_Proj.png?) 
18. Host the doc on ReadTheDocs
    - go to: [ReadTheDocs](https://readthedocs.org/).
    - create an account
    - import a project (add your github account to readTheDocs)
    ![Exported files](PICS/RTD_Import.png?) 
    - build the latest version  
19. Done! Your doc are now on the internet!

# How do i update my documentation? 
1. Run the steps 9 - 11
2. Upload the exported files into the source github repo (delete the old files) 
   - Can be done through te internet OR with step 17
3. Rebuild the docs on readthedocs.org (should also happen automatically!)