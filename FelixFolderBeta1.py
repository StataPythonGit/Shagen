'''
Created on 24.05.2014

@author: feli87
'''
#!/usr/bin/env python

import os
import re
import sys

import subprocess

	
def which(name, flags=os.X_OK):
	    """Search PATH for executable files with the given name.
12	   
13	    On newer versions of MS-Windows, the PATHEXT environment variable will be
14	    set to the list of file extensions for files considered executable. This
15	    will normally include things like ".EXE". This fuction will also find files
16	    with the given name ending with any of these extensions.
17	
18	    On MS-Windows the only flag that has any meaning is os.F_OK. Any other
19	    flags will be ignored.
20	   
21	    @type name: C{str}
22	    @param name: The name for which to search.
23	   
24	    @type flags: C{int}
25	    @param flags: Arguments to L{os.access}.
26	   
27	    @rtype: C{list}
28	    @param: A list of the full paths to files found, in the
29	    order in which they were found.
30	    """
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

def InitializeGit(git_directory=None):
    if os.path.exists("%s" %git_directory)==False:
        print "can't find git"        
    else:
        execGitCommand("%s add -A" %git_directory, True)
        execGitCommand("%s commit -m 'first commit'" %git_directory, True)
        print "you are all set up on git"

        #git_choice = raw_input("Do you want to use GitHub (y/n):")
        #if git_choice=="y":
         #   git_hub = raw_input("what is the link to your github?:")
          #  user = raw_input("what is your github username?:")
           # passw = raw_input("what is your github password?:")
    
            #try:
             #   execGitCommand("%(dir)s/git remote add origin %(hub)s" %dict(dir=git_directory, hub=git_hub) , True)
              #  execGitCommand("%s/git push origin master" %git_directory, True)
            #finally:
             #   execGitCommand("%(dir)s/git remote set-url origin %(hub)s| %(user)s | %(passw)s" %dict(dir=git_directory, hub=git_hub, user=user, passw=passw) , True)
              #  execGitCommand("%s/git push origin master" %git_directory, True)


       # else:
def stripcolon(text):
    text=r'%s' %text
    text=text.strip()    
    text=text.strip('"')    
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

def Gitcommit(git_directory=None, repository=None, files=None):
    if os.path.isfile(git_directory):
        execGitCommand(r"%s init" %git_directory, True)
        print "git found on computers program directory"
        #for m in files:
        #    file_location="%s/%s" %(repository, m)
        #    execGitCommand("%s add '%s'.do'" %(git_directory, file_location), True)  
        #    print "file added to git"
        append = """\n\n shell cd "$do_path" \n shell %s add -A \n shell %s commit -m 'version $datum'""" %(git_directory, git_directory)
        os.chdir(repository)
        open("0-master.do" , "a").write(append) 
        #f.close()
        InitializeGit(git_directory) 
        return git_directory 
    else:
        print "git not found"
        return False    

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
        pr = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = pr.stdout.read()
        err = pr.stderr.read()
        if err:
            print err
        if verbose and msg:
            print "Executing '%s'\n %s" % (command, colorText('red', 'Result:\n%s' % msg))
        return msg, err
    






# Ask the user for name
name = raw_input("Enter a project name:")
while name=="":
    name = raw_input("The name has to be non empty - duh, or q for quit:")
    if name=="q":
        sys.exit("set up aborted")
directory="False"
GitFound=False

#ask user for directory to set up folders
while os.path.exists(directory)==False:
    directory = raw_input('Enter the directory where folders should be set up (e.g. /Users/USERNAME/Documents) or q for quit: ')    
    if directory=="q":
        sys.exit("set up aborted")
    directory=stripcolon(directory)
    directory=os.path.expanduser(directory)
    print directory
    exist= os.path.exists(directory)
    print "exists:", exist


if os.path.exists(directory):
    print 'mkdir %(dir)s / %(name)s' %{"dir": directory ,"name":name}
    # Set up the echo command and direct the output to a pipe
    os.chdir(r'%s' %directory)
    os.mkdir(name)
    directory= directory + "/" +name
    mains=['build', 'analysis']
    git_location="False"
    for j in mains:
        os.chdir(r'%s' %directory)
        os.mkdir(j)
        folder=['input', 'code', 'output', 'temp', 'log']
        temp_dir= directory + '/' + j
        os.chdir(temp_dir)
        for s in folder:
            os.mkdir(s)
            print "created folder in %s" %temp_dir

        files=['0-master','1-preparation','2-regressions']   
        os.chdir(temp_dir + '/' + 'code')
        for m in files:
            f=open("%s.do" %m, "w+")
            if m=="0-master":
                    basics="""/*************************************************/ \n/*************************************************/ \n/****************  %s  ***************/ \n/*************************************************/ \n/*************************************************/ \n\nclear \ngraph set print logo off \n \ngraph set print tmargin 1 \ngraph set print lmargin 1\nset more off, perm\nset emptycells drop\n\nclear\nclear matrix\nset matsize 800\n\nset memory 4g\nset varabbrev on\n\n/*********************************************************\n*************         Master File     ********************\n*********************************************************\n\n**********************************\n**Change paths********************\n**********************************/\n\nglobal root "%s" \nglobal do_path "$root/code"\nglobal input_data_path "$root/input"\nglobal output_path "$root/output"\nglobal log_path "$root/log"\nglobal datum = subinstr(c(current_date)," ","",.)\n\n**********************************\n**Run Do-Files********************\n**********************************\n\n\ncd "$log_path"\ncap log close\nlog using preparation${datum}, replace\n\ncd "$do_path"\ndo 1-preparation\ncap log close\n\ncd "$log_path"\ncap log close\nlog using regressions${datum}, replace\n\ncd "$do_path"\ndo 2-regressions\ncap log close """ %(name, temp_dir)
                    f.write(basics)
            f.close()
            print "created file  %s.do" %m
#start the git set up process    
    for j in mains:  
        print "setting up git"
        
        repository  = "%(dir)s/%(folder)s/code" %{"dir": directory ,"folder":j}
        print repository
        if os.path.exists(repository):
            os.chdir(repository)
            git_init=execGitCommand(r"git init")                
            print git_init
            if os.path.isfile(git_location):
				GitFound=Gitcommit(git_location, repository, files)

            if GitFound==False & sys.platform =='darwin':
				print "running mac OS"
				git_location=which("git") 
				print git_location
				os.chdir(repository)
				GitFound=Gitcommit(git_location, repository, files)   
				
            if GitFound==False & sys.platform =='win32':
				print "running mac OS"
				git_location=check_output("where git/bin/git", shell=True)
				print git_location
				os.chdir(repository)
				GitFound=Gitcommit(git_location, repository, files)     				
			
            if GitFound==False:
				print "searching git"
				git_lcoation=execGitCommand(r"which git")                
				print git_location
				GitFound=Gitcommit(git_location, repository, files)
            if GitFound==False:
                #try to search the standard install directory on a MAC
                GitFound=Gitcommit("/usr/local/git/bin/git", repository, files) 
                git_location="/usr/local/git/bin/git"

            if GitFound==False:
                git_location="False"
                while os.path.isfile(git_location)==False:
                    print "location of git not found"
                    git_location = raw_input(r"where did you install git (pls enter the full directory of git.exe e.g. C:\appdata\local\programs\git\bin\git ) or q to skip git set up?:")
                    print git_location  
                    git_location = git_location + "\git.exe"
                    git_location = stripcolon(git_location)
                    print git_location                    
                    if  git_location=='"q"':
                        sys.exit("git not set up, but folders created")
                    GitFound=Gitcommit(git_location, repository, files)
            if GitFound==True:
                print "Git found"
        else:
            print "OS path doesn't seem to exist"

  
                                        



        
                
                        
