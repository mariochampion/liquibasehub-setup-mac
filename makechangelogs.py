#!/usr/bin/env python
'''
make a bunch of changelogs with changesets in a directory, for load testing liquibase hub

'''

## ===================================================================
## LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/liquibase-drift-reports
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
##
## Latest Liquibase Release: https://github.com/liquibase/liquibase/releases
## Contribute code to Liquibase: https://github.com/liquibase/liquibase
##
## please open issues and pull requests,
## thanks and always remember: this robot loves you. 
## boop boop!
## ===================================================================



################################# love your library(s)
import os, sys, subprocess, time, random


######### OVERALLCONFIGS
### TOOL VARS
toolname = "python_gen_tool"
toolversion = str("_v.12")

## TODO: MAKE THESE INTERACTIVE INPUTS
#num_of_files = int(5)
#num_of_changesets = int(5)
thistime = time.strftime("%H%M%S")

## DIR FOR CHANGELOG FILES AND .PROPERTIES FILES
dir_prefix = "loadtest"

### CHANGESET VARS
authorname = "mmc"
authorid = "create-table"
comment = toolname + toolversion
tablename_pre = "shnerb"

### CHANGELOG VARS
changelog_pre = "changelog00"
db_shortcode = "h2"
changelog_type = "sql"
sql_format_starter = "-- liquibase formatted sql "

### LIQUIBASE PROPERTIES FILE VARS
lbpropsfile_pre = "liquibase"
lbpropsfile_sfx = ".properties"
lbprops = lbpropsfile_pre + lbpropsfile_sfx
hubmodes_list = ("off","meta","all")
hubmode_default = "all"
hubapikey = os.environ.get('LIQUIBASE_HUB_APIKEY')
huburl = os.environ.get('LIQUIBASE_HUB_URL')
hubchangelogid = os.environ.get('LIQUIBASE_HUB_CHANGELOGID')
if hubapikey == "" or huburl == "" or hubchangelogid== "":
	print("DOH! Need both a LIQUIBASE_HUB_APIKEY and LIQUIBASE_HUB_URL and LIQUIBASE_HUB_CHANGELOGID for this to work.")
	print("Check the README for instructions!")
	sys.exit(1)

lbcmds_list = ("update") # not sure what else makes sense for this test for now


### WORKTIME TRACKING FILE VARS
worktimefile_suffix = "-worktime.csv"
worktime_fields = "action,hubmode,start,end,elapsed"
timefile = "total_time.csv"

#################################
## add a changeset to the changelog
def add_changeset(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter):
	
	authorid = authorid + "-" + thisincrement + "-" + thiscounter
	choice = random.choice(["company", "pizza"])
	tablename = tablename_pre + "" + choice + "" + thisincrement + "" + thiscounter
	
	if choice == "company":
		f.write("-- changeset " + authorname + ":" + authorid + "\r\n")
		f.write("-- comment: " + comment + "\r\n")
		f.write("create table " + tablename + " (\r\n")
		f.write("    id int primary key,\r\n")
		f.write("    name varchar(255) not null,\r\n")
		f.write("    address1 varchar(255),\r\n")
		f.write("    address2 varchar(255),\r\n")
		f.write("    city varchar(30)\r\n")
		f.write(")\r\n")
	else:
		f.write("-- changeset " + authorname + ":" + authorid + "\r\n")
		f.write("-- comment: " + comment + "\r\n")
		f.write("create table " + tablename + " (\r\n")
		f.write("    id int primary key,\r\n")
		f.write("    cheese varchar(255) not null,\r\n")
		f.write("    inches varchar(255),\r\n")
		f.write("    topping varchar(255),\r\n")
		f.write("    rainbows int(5)\r\n")
		f.write(")\r\n")	
	
	f.write("\r\n")
	



#################################
## make a liquibase.properties

def add_liquibaseproperties(changelogtoadd, lbp_increment, hubmode):
	lbp = open(lbpropsfile_pre + "-0" + lbp_increment + lbpropsfile_sfx, "w+")
	
	# Enter the path for your changelog file.
	lbp.write("changeLogFile=" + changelogtoadd + "\r\n")
	
	#### Enter the Target database 'url' information  ####
	lbp.write("url=jdbc:h2:tcp://localhost:9090/mem:dev\r\n")
	
	# Enter the username for your Target database.
	lbp.write("username: dbuser\r\n")
	
	# Enter the password for your Target database.
	lbp.write("password: letmein\r\n")
	
	#### Enter the Source Database 'referenceUrl' information ####
	## The source database is the baseline or reference against which your target database is compared for diff/diffchangelog commands.
	
	# Enter URL for the source database
	lbp.write("referenceUrl: jdbc:h2:tcp://localhost:9090/mem:integration\r\n")
	
	# Enter the username for your source database
	lbp.write("referenceUsername: dbuser\r\n")
	
	# Enter the password for your source database
	lbp.write("referencePassword: letmein\r\n")
	
	
	#### HUB INFO
	lbp.write("liquibase.hub.apikey:" +hubapikey+ "\r\n")
	lbp.write("liquibase.hub.url:" +huburl+ "\r\n")
	lbp.write("liquibase.hub.mode:" +hubmode+ "\r\n")
	
	lbp.write("\r\n")
	lbp.close()





######################################
## make a dir to store things in	

def make_loadtestdir(num_of_files, num_of_changesets):
	dir_name = dir_prefix + "_" + str(num_of_files)+ "x" +str(num_of_changesets)+ "_" + str(thistime)
	dir_parent = "./"
	dir_path = os.path.join(dir_parent, dir_name)
	os.mkdir(dir_path, 0o777)
	os.chdir(dir_path)
	print(color.cyan + "DONE: DIR CREATED" +dir_path+ "\r\n" + color.white )
	
	return dir_name




######################################
## create a number of changelogfiles
def make_changelogfiles(num_of_files, num_of_changesets, hubmode):
	for a in range(num_of_files):
	
		## SETUP SOME VARS
		thisincrement = str((a+1))
		changelogname = changelog_pre
		changelogtoadd = changelog_pre + thisincrement + "_"+str(num_of_changesets)+"_changes." +db_shortcode+ "." + changelog_type
		
		
		
		print("START MAKING FILES")	
		#start the file
		f = open( changelogtoadd,"w+" )
		f.write( sql_format_starter + " changelogid:" + str(hubchangelogid) + "\r\n")
		f.write("\r\n")
		
		
		for b in range(num_of_changesets):
			thiscounter = str(b + 1)
			add_changeset(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter)
		f.close() 
	
		#### while it could be argued for these to be decoupled, they are convenient here for now
		## make a liquibase.properties file
		add_liquibaseproperties(changelogtoadd, thisincrement, hubmode)
		
				
		## give an update
		print(color.cyan + "DONE: generated " +changelogtoadd+ " with " +str(num_of_changesets)+ " changesets.\r\n" + color.white )
		
	




######################################
## dcreate a file for tracking timestamps in
def add_worktimefile(changelogtoadd):
	
	## setup some vars
	worktimefile = changelogtoadd + worktimefile_suffix
	
	## create the file for later adding timestamps
	lf = open (worktimefile, "w+")
	lf.write(worktime_fields + "\n")
	lf.close()
	
	return worktimefile
	



######################################
## do the initial main work
def main(args):
	
	#iterate thru args passed on command line, could be 0 - 4
	lbcmd = "none"
	do_lbcmd = 0
	hubmode = hubmode_default
	total_time = 0
	starth2 = 0

	if len(args) == 0:
		print(color.yellow + "No parameters found. Please answer two quick questions:" + color.white)		
		num_of_files = input(color.yellow + "In this loadtest, how many changelogs? \r\n" + color.white)		
		num_of_changesets = input(color.yellow + "and in each, how many changesets? \r\n" + color.white)		

	if len(args) == 2:
		num_of_files = args[0]
		num_of_changesets = args[1]		
		print(color.cyan + "Done: Changelog and changeset quantities set.\r\n" + color.white)
		
		#ask for other two optional params		
		lbcmd_raw = raw_input("Optional: Auto-run liquibase update command? Enter [y] or [n] \r\n")
		if lbcmd_raw in ("y","Y"):
			lbcmd = "update"
			do_lbcmd = 1
		if lbcmd_raw in ("n","N"):
			lbcmd = "none"		
		
		
		send_data_raw = raw_input("Optional: Send command reports to Hub? Enter [y] or [n] \r\n")
		if send_data_raw in ("y","Y"):
			hubmode = "all"
		if send_data_raw in ("n","N"):
			hubmode = "off"	
			
		starth2_raw = raw_input("Optional: Start local in-memory H2 db? Enter [y] or [n] \r\n")
		if starth2_raw in ("y","Y"):
			starth2 = 1
		if starth2_raw in ("n","N"):
			starth2 = 0	

	if len(args) == 3:
		num_of_files = args[0]
		num_of_changesets = args[1]	
		if args[2] in lbcmds_list: ## this is weird, do i need?
			lbcmd = args[2]
			do_lbcmd = 1
		else:
			print("whoa -- only valid 3rd param for now is 'update'.")
			sys.exit(1)
		

	if len(args) == 4:
		num_of_files = args[0]
		num_of_changesets = args[1]
		if args[2] in lbcmds_list: ## this is weird, do i need?
			lbcmd = args[2]
			do_lbcmd = 1
		else:
			print("whoa -- only valid 3rd param for now is 'update'.")
			sys.exit(1)
			
		if args[3] in hubmodes_list:
			hubmode = args[3]
			do_hubsend = 1
		else:
			do_hubsend = 0
	else:
		do_hubsend = 0
		
		
	##perhaps this belongs some other place but lets try a start-h2
	if starth2 == 1:
		print(color.red + "\r\n------ STARTING h2 DATABASE -------\r\n" + color.white)
		newtabcmd="./start-h2"
		subprocess.Popen(newtabcmd, shell=True)
	
	
	
	## now do some variable type checking, 'cause...  
	try:
		num_of_files = int(num_of_files)
	except: 
		print "doh! NUMBERS ONLY for number of changelog files and number of changesets in them."
		print("Check the README for instructions!")
		sys.exit(1)
      
	try:
		num_of_changesets = int(num_of_changesets)
	except: 
		print "doi! NUMBERS ONLY for number of changelog files and number of changesets in them."
		print("Check the README for instructions!")
		sys.exit(1)
	

	
	##show some configs
	print("CONFIG'ED ARGS: liquibase command: " + lbcmd + " | hubmode: " + hubmode)
	
	######## DO ALL THE WORK
	##make the dir and keep the name
	loadtest_dir = make_loadtestdir(num_of_files, num_of_changesets)	
	
	## make the changelog files w/ changesets AND liquibase.properties files
	make_changelogfiles(num_of_files, num_of_changesets, hubmode)
	
	
	
	## do the commands
	if do_lbcmd == 1:
		total_time = dolbcommand(loadtest_dir, num_of_files, num_of_changesets, lbcmd, hubmode)
	
	
	
	
	### do teh closing
	total_commands = int(num_of_files)*int(num_of_changesets)
	do_teh_closing(total_time, total_commands)





######################################
## do the update command, cycling thru the liquibase.properties files
## perhaps move this to a different file, so it could be useful and called outside this script
## for now, just limit to update because of simplicity and not checking all known lb commands etc
def dolbcommand(loadtest_dir, num_of_files, num_of_changesets, lbcmd, hubmode):
	print("Moved to " + loadtest_dir + " with " + str(num_of_files)+ " changelogs and .props files")
	
	status_prestart = time.time()	
	for thisprop in range(num_of_files):
		# construct filename TODO: use the vars!
		total_commands = int(num_of_files)*int(num_of_changesets)
		worktimefile = "changelog0" + str(thisprop+1) + worktimefile_suffix
		thispropsfile = "liquibase-0" + str(thisprop+1) + lbpropsfile_sfx
		print(color.blue + "START: Processing: " + thispropsfile + color.white + "\r\n")
		
		os.rename(thispropsfile, lbprops)
		
		## start tracking
		## worktime_fields = action,hubmode,start,end,elapsed
		status_start = time.time()		
		
		# now do the liquibase command
		# assume for now that h2 is running from external sources etc
		# do this hard-coded, but this/these could passed in from params
		statuscmd = "liquibase status"
		subprocess.call(statuscmd, shell=True)
		time.sleep(3) 
		print(color.cyan + "\r\n------ (DONE: STATUS) -------\r\n" + color.white)
	
		status_end = time.time()
		lbcmd_start = time.time()
	
		## DO THE COMMAND
		updatecmd = "liquibase " + lbcmd
		subprocess.call(updatecmd, shell=True) 
		print(color.cyan + "\r\n------ (DONE: UPDATE) -------\r\n" + color.white)
	
		lbcmd_end = time.time()	
		wrk = open(worktimefile, "a+")
		wrk.write(worktime_fields + "\n")
		wrk.write("status," +hubmode+ "," + str(status_start) + "," + str(status_end) + "," + str(status_end-status_start) + "\n")
		wrk.write(lbcmd + "," + hubmode + "," + str(lbcmd_start) + "," + str(lbcmd_end) + "," + str(lbcmd_end-lbcmd_start) + "\n")
		wrk.close()
		#rename the props file to keep for later runs
		os.rename(lbprops, thispropsfile)
	
	##prep for the totals
	total_time = lbcmd_end-status_prestart	
	tt = open(timefile, "w+")
	tt.write("total_commands,total_time \n")
	tt.write(str(total_commands) +","+ str(total_time) )
	tt.close()
	
	return total_time


	
	
######################################
## just a little closer
def do_teh_closing(total_time, total_commands):
	## first stop h2
	endH2cmd="killall java"
	subprocess.Popen(endH2cmd, shell=True)
	
	## then present the good news!
	print(color.magenta + "------------------------------------------" + color.white)
	print("\r")
	print(color.cyan + " -- Completed: " +str(total_commands)+" commands in " +str(total_time)+ " seconds-- " + color.white)
	print("\r")
	print(color.cyan + "     ps. i love you. boop.boop." + color.white)
	print("\r")
	print(color.magenta + "------------------------------------------\r" + color.white)

	sys.exit(1) 




#######################################
## ADD SOME COLOR
# pinched and tweaked from https://github.com/impshum/Multi-Quote/blob/master/run.py
class color:
  white, cyan, blue, red, green, yellow, magenta, black, gray, bold = '\033[0m', '\033[96m','\033[94m', '\033[91m','\033[92m','\033[93m','\033[95m', '\033[30m', '\033[30m', "\033[1m"  

# maybe add bks, bolds, etc from https://godoc.org/github.com/whitedevops/colors
class bkcolor:
  resetall = "\033[0m"
  default      = "\033[49m"
  black        = "\033[40m"
  red          = "\033[41m"
  green        = "\033[42m"
  yellow       = "\033[43m"
  blue         = "\033[44m"
  magenta      = "\033[45m"
  cyan         = "\033[46m"
  lightgray    = "\033[47m"
  darkgray     = "\033[100m"
  lightred     = "\033[101m"
  lightgreen   = "\033[102m"
  lightyellow  = "\033[103m"
  lightblue    = "\033[104m"
  lightmagenta = "\033[105m"
  lightcyan    = "\033[106m"
  white        = "\033[107m"



	
############## GET STARTED	

#################################
# boilerplate kicker offer (yes thats a tech term!)   
if __name__ == '__main__':
  
  try:
    args
  except:
    args = sys.argv[1:]
  
  main(args)






	
	
	
	