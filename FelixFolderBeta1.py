'''
Created on 24.05.2014

@author: feli87
'''
#!/usr/bin/env python

import os
import re
import sys
import subprocess
from distutils import spawn


# Functions to search for git on computer
def which(name, flags=os.X_OK):
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Make things pretty functions
def stripcolon(text):
    text=r'%s' %text
    text=text.strip()
    text=text.strip('"')
    if text.endswith('/'):
        text=text[:-1]
    text=text.replace('\\',"/")
    #text='"'+text+'"'
    return text

def colorText(color, text):
    colorCodes = {
        'black':'30',
        'red':'31',
        'green':'32',
        'yellow' :'33',
        'blue':'34',
        'magenta' :'35',
        'cyan' :'36',
         'white ' :'37',
        }

    return "\x1b[%sm%s\x1b[m" % (colorCodes[color], text)

# Functions that set up git
def GitSetUp(git_directory=None, repository=None, files=None, name=None, temp_dir=None):
    if os.path.isfile(git_directory):
        execGitCommand(r"%s init" %git_directory, True)
        print "git found on computers program directory"
        doFileCreator(repository, name, git_directory, temp_dir)
        GitBackUp(git_directory)
        return git_directory
    else:
        print "git not found"
        return False


def GitBackUp(git_directory=None):
    if os.path.exists("%s" %git_directory)==False:
        print "can't find git"
    else:
        execGitCommand("%s add -A" %git_directory, True)
        execGitCommand('%s commit -m "first commit"' %git_directory, True)
        print "you are all set up on git"


def execGitCommand(command=None, verbose=False):
    """    Function used to get data out of git commads
        and errors in case of failure.

        Args:
            command(string): string of a git command
            verbose(bool): whether to display every command
            and its resulting data.
        Return:
            (tuple): string of Data and error if present
    """
    if command:
        # converts multiple spaces to single space
        command = re.sub(' +',' ',command)
        if sys.platform =='darwin':
            pr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if sys.platform =='win32':
            pr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = pr.stdout.read()
        err = pr.stderr.read()
        if err:
            print err
        if verbose and msg:
            print "Executing '%s'\n %s" % (command, msg)
        return msg, err

def doFileCreator(repository=None, name=None, git_directory=None, project_dir=None):
    os.chdir(repository)
    files=['0-master','1-preparation','2-regressions']
    task_folder = os.path.basename(os.path.dirname(repository))
    for m in files:
        f=open("%s.do" %m, "w+")
        if m=="0-master" and task_folder == "build":
            basics=("""/*************************************************/ \n"""
                    """/*************************************************/ \n"""
                    """/****************  %(name)s  ***************/ \n"""
                    """/*************************************************/ \n"""
                    """/*************************************************/ \n \n  \n \n \n"""
                    """clear \ngraph set print logo off \n \n"""
                    """graph set print tmargin 1 \n"""
                    """graph set print lmargin 1\n"""
                    """set more off, perm\n"""
                    """set emptycells drop\n\n"""
                    """clear\n"""
                    """clear matrix\n"""
                    """set matsize 800\n\n"""
                    """set varabbrev on\n\n/"""
                    """*********************************************************\n"""
                    """*************         Master File     ********************\n"""
                    """*********************************************************\n\n"""
                    """**********************************\n"""
                    """**Change paths********************\n"""
                    """**********************************/\n\n"""
                    """if regexm(c(os),"Mac") == 1 {\n"""
                    """    global root "%(root)s" \n"""
                    """    }\n"""
                    """else if regexm(c(os),"Windows") == 1 {\n"""
                    """    global root "%(root)s" \n"""
                    """}\n"""
                    """global do_path "$root/%(task)s/code"\n """
                    """global input_path "$root/%(task)s/input"\n """
                    """global temp_path "$root/%(task)s/temp"\n """
                    """global output_path "$root/%(task)s/output"\n """
                    """global log_path "$root/%(task)s/log"\n """
                    """global datum = subinstr(c(current_date)," ","",.)\n"""
                    """cd "$input_path" \n"""
                    """/**************** Version Controll ******************************/ \n \n"""
                    """shell \"%(git)s\" --git-dir "$do_path/.git" --work-tree "$do_path/." commit -a -m "version $datum" \n\n\n"""
                    """**********************************\n"""
                    """**Run Do-Files********************\n"""
                    """**********************************\n\n\n"""
                    """cd "$log_path"\n"""
                    """cap log close\n"""
                    """log using preparation${datum}, replace\n\n"""
                    """cd "$do_path"\ndo 1-preparation\n"""
                    """cap log close\n\n"""
                    """cd "$log_path"\n"""
                    """cap log close\n"""
                    """log using regressions${datum}, replace\n\n"""
                    """cd "$do_path"\ndo 2-regressions\n"""
                    """cap log close """) %{"git": git_directory, "task": task_folder, "root": project_dir, "name": name}
            f.write(basics)
        if m=="0-master" and task_folder == "analysis":
            basics=("""/*************************************************/ \n"""
                    """/*************************************************/ \n"""
                    """/****************  %(name)s  ***************/ \n"""
                    """/*************************************************/ \n"""
                    """/*************************************************/ \n \n  \n \n \n"""
                    """clear \ngraph set print logo off \n \n"""
                    """graph set print tmargin 1 \n"""
                    """graph set print lmargin 1\n"""
                    """set more off, perm\n"""
                    """set emptycells drop\n\n"""
                    """clear\n"""
                    """clear matrix\n"""
                    """set matsize 800\n\n"""
                    """set varabbrev on\n\n/"""
                    """*********************************************************\n"""
                    """*************         Master File     ********************\n"""
                    """*********************************************************\n\n"""
                    """**********************************\n"""
                    """**Change paths********************\n"""
                    """**********************************/\n\n"""
                    """if regexm(c(os),"Mac") == 1 {\n"""
                    """    global root "%(root)s" \n"""
                    """}\n"""
                    """else if regexm(c(os),"Windows") == 1 {\n"""
                    """    global root "%(root)s" \n"""
                    """}\n"""
                    """global do_path "$root/%(task)s/code"\n """
                    """global input_path "$root/%(task)s/input"\n """
                    """global temp_path "$root/%(task)s/temp"\n """
                    """global output_path "$root/%(task)s/output"\n """
                    """global log_path "$root/%(task)s/log"\n """
                    """global datum = subinstr(c(current_date)," ","",.)\n"""
                    """cd "$input_path" \n"""
                    """/**************** Version Controll ******************************/ \n \n"""
                    """shell \"%(git)s\" --git-dir "$do_path/.git" --work-tree "$do_path/." commit -a -m "version $datum" \n\n\n"""
                    """**copy files from build output\n"""
                    """**windows\n"""
                    """if c(os) == "Windows" {\n"""
                    """ shell xcopy "$root/build/output" "$input_path" /I /S\n"""
                    """}\n"""
                    """**OS\n"""
                    """if c(os) == "MacOSX" {\n"""
                    """ !mv -f "$root/build/output/"* "$input_path/" \n"""
                    """}\n"""
                    """**********************************\n"""
                    """**Run Do-Files********************\n"""
                    """**********************************\n\n\n"""
                    """cd "$log_path"\n"""
                    """cap log close\n"""
                    """log using preparation${datum}, replace\n\n"""
                    """cd "$do_path"\ndo 1-preparation\n"""
                    """cap log close\n\n"""
                    """cd "$log_path"\n"""
                    """cap log close\n"""
                    """log using regressions${datum}, replace\n\n"""
                    """cd "$do_path"\ndo 2-regressions\n"""
                    """cap log close """) %{"git": git_directory, "task": task_folder, "root": project_dir, "name": name}
            f.write(basics)
        if m=="1-preparation":
            basics=("""/*************************************************/ \n"""
                    """/*************************************************/ \n"""
                    """/****************  %s  ***************/ \n"""
                    """/*************************************************/ \n"""
                    """/*************************************************/ \n \n \n \n \n"""
                    """/**************** Version Controll ******************************/ \n \n"""
                    """shell \"%s\" --git-dir "$do_path/.git" --work-tree "$do_path/." commit -a -m "version $datum" \n \n\n"""
                    """clear \n\n\n"""
                    """/*********************************************************\n"""
                    """*************         Preparation File     ********************\n"""
                    """*********************************************************/\n\n\n"""
                    """global datum = subinstr(c(current_date)," ","",.)\n\n""") %(name, git_directory)
            f.write(basics)
        if m=="2-regressions":
            basics=("""/*************************************************/ \n/"""
                    """*************************************************/ \n"""
                    """/****************  %s  ***************/ \n"""
                    """/*************************************************/ \n"""
                    """/*************************************************/ \n \n \n \n \n"""
                    """/**************** Version Controll *****************************/ \n\n"""
                    """shell \"%s\" --git-dir "$do_path/.git" --work-tree "$do_path/." commit -a -m "version $datum" \n \n\nclear \n"""
                    """/*********************************************************\n"""
                    """*************         Regressions File     ********************\n"""
                    """*********************************************************/\n\n\n"""
                    """global datum = subinstr(c(current_date)," ","",.)\n\n""") %(name, git_directory)
            f.write(basics)
            f.close()
            print "created file  %s.do" %m


def getname():
    name = raw_input("Enter a project name:\n")
    while name=="":
        name = raw_input("The name has to be non empty - duh, or q for quit:")
    if name=="q":
        sys.exit("set up aborted")
    return name

# %%

###############################################################################
###############################################################################
#################       project name & place            #######################
###############################################################################
###############################################################################


# Ask the user for name
name=getname()
directory="False"
GitFound=False

#ask user for directory to set up folders
while os.path.exists(directory)==False:
    directory = raw_input('Enter the directory where folders should be set up (the path to the folder where you keep your research projects e.g. /Users/USERNAME/Documents) or q for quit: \n')
    if directory=="q":
        sys.exit("set up aborted")
    directory=stripcolon(directory)
    directory=os.path.expanduser(directory)
    print directory
    exist= os.path.exists(directory)
    print "exists:", exist
    if os.path.exists(directory + "/" +name):
        directory=""
        print "\n this folder name already exists \n"
        name=getname()



# %%

###############################################################################
###############################################################################
####################          create folders        ###########################
###############################################################################
###############################################################################



if os.path.exists(directory):
    print 'mkdir %(dir)s / %(name)s' %{"dir": directory ,"name":name}
    os.chdir(r'%s' %directory)
    os.mkdir(name)
    directory = os.path.join(directory , name)
    mains=['build', 'analysis']
    git_location="False"
    for j in mains:
        os.chdir(r'%s' %directory)
        os.mkdir(j)
        folder=['input', 'code', 'output', 'temp', 'log']
        files=['0-master','1-preparation','2-regressions']
        temp_dir= directory + '/' + j
        os.chdir(temp_dir)
        for s in folder:
            os.mkdir(s)
            print "created folder in %s" %temp_dir

# %%

###############################################################################
###############################################################################
####################          GIT set up            ###########################
###############################################################################
###############################################################################


    #start the git set up process
    for j in mains:
        print "setting up git"

        repository  = "%(dir)s/%(folder)s/code" %{"dir": directory ,"folder":j}
        print repository
        if os.path.exists(repository):
            os.chdir(repository)

            if GitFound!=False:
                git_location=GitFound
                GitFound=GitSetUp(git_location, repository, files, name, directory)
                continue

            if GitFound==False and sys.platform =='darwin':
                #try to search the standard install directory on a MAC
                GitFound=GitSetUp("/usr/local/git/bin/git", repository, files, name, j)
                git_location="/usr/local/git/bin/git"


            if GitFound==False and sys.platform =='darwin':
                print "running mac OS"
                try:
                    git_location=which("git")
                    print git_location
                except IOError:
                    print 'cannot find git'
                os.chdir(repository)
                if type(git_location)==str:
                    GitFound=GitSetUp(git_location, repository, files, name, j)
                elif type(git_location)==list:
                    for i in git_location:
                        if '/bin/git' in i:
                            git_location=i
                            GitFound=GitSetUp(git_location, repository, files, name, j)
                        else:
                            print ""
                else:
                    print "We just can't fing GIT anywhere..."
                    print "Variable type that was returned by our search"
                    print type(git_location)

            if GitFound==False and sys.platform =='win32':
                print "running Windows"
                try:
                    git_location=subprocess.check_output("where git.exe", stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    print e.output
                    print git_location
                    pass
                if type(git_location)==str and git_location!="False":
                    git_location_templist = git_location.split("Git")
                    git_location = git_location_templist[0]+r'\bin\git.exe'
                    print git_location
                    os.chdir(repository)
                    GitFound=GitSetUp(git_location, repository, files, name, j)
                if type(git_location)==list and git_location!="False":
                    for i in git_location:
                        try:
                            git_location_templist = git_location.split("Git")
                            git_location = git_location_templist[0]+r'\bin\git.exe'
                            print git_location
                            os.chdir(repository)
                            GitFound=GitSetUp(git_location, repository, files, name, j)
                        except:
                            print i
                if type(git_location)!=list and type(git_location)!=str and git_location!=False:
                    print "What kind of weird file structure is that? I found this directory:"
                    print git_location


            if GitFound==False:
                git_location="False"
                while os.path.isfile(git_location)==False:
                    print "\n We couldn't find GIT on your computer. \n\n If you haven't installed GIT:\n Read ch.3 of Gentzkow & Shapiro on version controll. Git will help you keep track of changes you made in your do files: It also allows you to go back to earlier versions of your work\n Best to follow the masters and go to www.git-scm.com/downloads and install GIT, its FREE \n"
                    if sys.platform =='darwin':
                        git_location = raw_input('If you already installed GIT: \n Can you tell us the directory of GIT (HINT: it will be in a folder called "bin" e.g. sth like usr/local/git/bin/git ) \n To skip setting up GIT press q:\n')
                        git_location = stripcolon(git_location)
                        if  git_location=='q':
                            doFileCreator(repository, name, git_location, j)

                            if j=="analysis":
                                sys.exit("All folders created, but GIT not set up")
                            continue
                        print git_location
                        git_location_templist = git_location.split("/")
                        if git_location_templist[len(git_location_templist)-1]!="git":
                            git_location = git_location + "/git"
                        print git_location
                        GitFound=GitSetUp(git_location, repository, files, name, j)
                    if sys.platform =='win32':
                        git_location = raw_input(r"If you already installed GIT: Can you tell us the directory of GIT (pls enter the full directory of git.exe e.g. C:\appdata\local\programs\git\bin\git ) \n or enter q to skip setting up GIT?:\n")
                        git_location = stripcolon(git_location)
                        if  git_location=='q':
                            for m in files:
                                doFileCreator(repository, name, git_location, j)
                            if j=="analysis":
                                sys.exit("All folders created, but GIT not set up")
                            continue

                        git_location = git_location + "\git.exe"
                        print git_location

                        GitFound=GitSetUp(git_location, repository, files, name, j)
            if GitFound!=False:
                print "Git found"
        else:
            print "OS path doesn't seem to exist"









