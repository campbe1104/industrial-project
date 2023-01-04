from datetime import datetime
import os
from os.path import exists


"""
Description:
 this script updates local copies of specified repos, 
 creates a custom configeration file for each repo then 
 runs doxygen on each local repo and saves them in an 
 output folder.
"""

#A list of all the repos to be used in the script is saved to repos array
repos = ["proj1","proj2","proj3","proj4","proj5","proj6",]


#Repository folder is created 
os.system("rm -r -f repositories") 
os.mkdir('repositories')

#Date is saved to today and turned into a string
today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#The absolute paths of the log file and the documentation folder are saved to variables
log_location = str(os.path.abspath("doxygen.log"))

documents_location = str(os.path.abspath("doxygen_documentation"))





#log_setup function is created
def log_setup():
   """This function clears the logs file then it is given a new header"""

   #the log file is cleared
   open(log_location, 'w').close()

   #The heading for the log file is created
   doxylog = open(log_location, 'a')   
   doxylog.write('logs from doxymated python script run on '+ today+'\n\n\n')
   doxylog.close()


   return documents_location
   







#Automation function is created
def automation():
   
   """This function runs a command that schedules this script to be run in 7 days form now"""

   #A command is run that makes the script run again in 7 days time  
   os.system ('echo "python doxymated.py"  | at now + 7 days')





#Clone_repos function is called
def clone_repos(i):

   """This function clears existing copies of repos then replaces them with up to date ones"""

   #outdated copies of repositories are removed if they exist
   os.system("rm -r -f " + i)

   os.mkdir(i)
   os.chdir(i)

   #The up to date repos are cloned

   os.system("git clone https://github.com/team/" + i) 



      






#This function creates the config file
def run_doxy (i):

   """This function creates the custom configeration 
   file along with running doxygen on each repo """



   #The placeholders from the template config file is saved to options array
   option = ['proj_name','proj_number','proj_brief','out_dir','project_lan_c','project_lan_java']


      #If the script is working on scripts repo config file is optimized for java
   if i == "proj3":
      java = "YES"
      c = "NO"

      #If script is not working on scripts config file is optimized for c
   else:
      java = "NO"
      c = "YES"

   #The log file is opened
   doxylog = open(log_location, 'a')

   #The contents of config file in the current working direcotory is cleared 
   open('doxyfile', 'w').close()


   #The template file is opened to be read
   fin = open("../../template_doxyfile", "rt")
   

   #The doxyfile in the current directory is opened to be written to 
   fout = open("doxyfile", "wt")
   

   #A loop is started that looks through each line looking for words to replace
   for line in fin:
      

      #The specified options are found then changed
      fout.write(line.replace(option[0] ,i)
      .replace(option[1],today)
      .replace(option[2],"\"automated documentation created for " +i+ " repository\"")
      .replace(option[3],documents_location +"/"+ i)
      .replace(option[4],c)
      .replace(option[5],java))

      
   #The template file is closed           
   fin.close()
   

   #The config file is closed
   fout.close()

   
   #If the config file exists config _exists changes to true
   config_exists = exists('doxyfile')

   #If the config file doesn't exist a message is saved in the log
   if config_exists == False:
      doxylog.write('The doxyflile for ' + i + ' repo faild to generate\n')
         
   else:

      #If doxygen runs successfully then a message is saved to the log file
      doxylog.write('The doxyfile for '+i+' was generated successfully\n\n')


      #Doxygen is run on the current directory using the custom config file
      os.system("doxygen doxyfile")

      #If doxygen runs successfully then a message is saved to the log file
      doxylog.write('doxygen was successfully run for '+i+' repo\n\n')



      #Current directory is changed to parent directory
      os.chdir("../")

   #The log file is closed
   doxylog.close()




#Main repo is created
def main():
   
   #Function is called to clear and add a header to log file
   log_setup()

   #Automation function is called
   automation()

   #The directory is changed to repositories
   os.chdir('repositories')
   
   for i in repos:

      #The function that updates teh repos is called
      clone_repos(i)

      #The function that creates a config file and runs doxygen is called
      run_doxy(i)
   



#Main function is run
if __name__ == "__main__":
    main()
