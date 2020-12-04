#!/usr/bin/env python
'''
make ONE changelogs with changesets in a directory, for load testing liquibase hub
and register it, and then take that projectid and add it to env var

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
toolversion = str("_v.r_01")

## TODO: MAKE THESE INTERACTIVE INPUTS
#num_of_files = int(5)
#num_of_changesets = int(5)
thistime = time.strftime("%H%M%S")

## DIR FOR CHANGELOG FILES AND .PROPERTIES FILES
dir_prefix = "regnewproject"

### CHANGESET VARS
authorname = "mmc"
authorid = "create-table"
comment = toolname + toolversion
tablename_pre = "gen"

### CHANGELOG VARS
changelog_pre = "changelog00"
db_shortcode = "h2"
changelogstypes_list = ("sql", "xml")
changelog_type_default = "sql"
sql_format_starter = "-- liquibase formatted sql "



### LIQUIBASE PROPERTIES FILE VARS
lbpropsfile_pre = "liquibase"
lbpropsfile_sfx = ".properties"
lbprops = lbpropsfile_pre + lbpropsfile_sfx
hubmodes_list = ("off","meta","all")
hubmode_default = "off"
hubapikey = os.environ.get('LIQUIBASE_HUB_APIKEY')
huburl = os.environ.get('LIQUIBASE_HUB_URL')
hubprojectid = os.environ.get('LIQUIBASE_HUB_PROJECTID')
if hubapikey == "" or huburl == "" or hubprojectid == "":
	print("DOH! Need 3 env vars:LIQUIBASE_HUB_APIKEY, LIQUIBASE_HUB_URL, LIQUIBASE_HUB_PROJID for this to work.")
	print("Check the README for instructions!")
	sys.exit(1)


#################################
## add a changeset to the changelog
def add_changeset_sql(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter):
	
	choice = random.choice(["company", "pizza"])
	authorid = authorid + "-" + choice + "-" +thisincrement + "-" + thiscounter
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
		
	f.write("-- rollback DROP TABLE " + tablename + "\r\n")	
	f.write("\r\n")
	




#################################
## start an xml changelog
def xml_format_starter(f):
	f.write('<?xml version="1.0" encoding="UTF-8"?>')
	f.write("\r\n")
	f.write("\r\n")
	f.write('<databaseChangeLog')
	f.write("\r\n")
	f.write('        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"')
	f.write("\r\n")
	f.write('        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
	f.write("\r\n")
	f.write('        xmlns:pro="http://www.liquibase.org/xml/ns/pro"')
	f.write("\r\n")
	f.write('        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.2.xsd http://www.liquibase.org/xml/ns/pro http://www.liquibase.org/xml/ns/pro/liquibase-pro-4.2.xsd">')
	f.write("\r\n")

	




#################################
## add a changeset to the changelog
def add_changeset_xml(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter):
	
	choice = random.choice(["company", "pizza"])
	authorid = authorid + "-" + choice + "-" +thisincrement + "-" + thiscounter
	tablename = tablename_pre + "" + choice + "" + thisincrement + "" + thiscounter
	
	if choice == "company":
		f.write('    <changeSet id="'+authorid+'" author="'+authorname+'">\r\n')
		f.write('        <createTable tableName="'+tablename+'">\r\n')
		f.write('            <column name="id" type="int">\r\n')
		f.write('                <constraints primaryKey="true"/>\r\n')
		f.write('            </column>\r\n')
		f.write('            <column name="name" type="varchar(50)">\r\n')
		f.write('                <constraints nullable="false"/>\r\n')
		f.write('            </column>\r\n')
		f.write('            <column name="address1" type="varchar(255)"/>\r\n')
		f.write('            <column name="address2" type="varchar(255)"/>\r\n')
		f.write('            <column name="city" type="varchar(128)"/>\r\n')
		f.write('        </createTable>\r\n')
		f.write('    </changeSet>')
		f.write("\r\n")
	else:
		f.write('    <changeSet id="'+authorid+'" author="'+authorname+'">\r\n')
		f.write('        <createTable tableName="'+tablename+'">\r\n')
		f.write('            <column name="id" type="int">\r\n')
		f.write('                <constraints primaryKey="true"/>\r\n')
		f.write('            </column>\r\n')
		f.write('            <column name="crust" type="varchar(50)">\r\n')
		f.write('                <constraints nullable="false"/>\r\n')
		f.write('            </column>\r\n')
		f.write('            <column name="inches" type="varchar(255)"/>\r\n')
		f.write('            <column name="topping" type="varchar(255)"/>\r\n')
		f.write('            <column name="sauce" type="varchar(128)"/>\r\n')
		f.write('        </createTable>\r\n')
		f.write('    </changeSet>')
		f.write("\r\n")

	
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
def make_changelogfiles(num_of_files, num_of_changesets, hubmode, changelog_type):
	for a in range(num_of_files):
	
		## SETUP SOME VARS
		thisincrement = str((a+1))
		changelogname = changelog_pre
		changelogtoadd = changelog_pre + thisincrement + "_"+str(num_of_changesets)+"_changes." +db_shortcode+ "." + changelog_type
		
		#start the file
		print("START MAKING FILES")	
		f = open( changelogtoadd,"w+" )		

		if changelog_type == "sql":		
			f.write( sql_format_starter + "\r\n")
			f.write("\r\n")

		if changelog_type == "xml":				
			xml_format_starter(f)
			f.write("\r\n")
		
		# add changeset
		for b in range(num_of_changesets):
			thiscounter = str(b + 1)
			if changelog_type == "sql":
				add_changeset_sql(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter)
			if changelog_type == "xml":
				add_changeset_xml(f, authorname, authorid, comment, tablename_pre, thisincrement, thiscounter)
				
		#add closing line in changelog file if XML
		if changelog_type == "xml":
			f.write('</databaseChangeLog>')	
			
		f.close() 
	
		#### while it could be argued for these to be decoupled, they are convenient here for now
		## make a liquibase.properties file
		add_liquibaseproperties(changelogtoadd, thisincrement, hubmode)
		
				
		## give an update
		print(color.cyan + "DONE: generated " +changelogtoadd+ " with " +str(num_of_changesets)+ " changesets.\r\n" + color.white )
		
	






######################################
## do the initial main work
def main(args):
	
	#iterate thru args passed on command line, could be 0 - 4
	lbcmd = "none"
	do_lbcmd = 0
	hubmode = hubmode_default
	changelog_type = changelog_type_default
	total_time = 0

	num_of_files = 1
	num_of_changesets = 1	
	print(color.cyan + "Done: Changelog and changeset quantities set.\r\n" + color.white)
		
	

	
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
	make_changelogfiles(num_of_files, num_of_changesets, hubmode, changelog_type)
	
	
	##check for one file to do special things if 'loadtest 1 1 [n] [y] [n]'
	if (int(num_of_files) == 1):
		#&& (int(num_of_changesets) == 1) && (hubmode == "all")
		print(color.cyan + "\r\n------ (SPECIAL REG NEW PROJECT (1)) -------\r\n" + color.white)
		os.rename("liquibase-01.properties", lbprops)
		
		# then register the changelog
		newprojectid = registernewproject()
		print(color.cyan + "\r\n------ (newprojectid: "+newprojectid+" -------\r\n" + color.white)
		envvarcmd="sh ../addEnvVarProjId.sh " + newprojectid
		subprocess.call(envvarcmd, shell=True)

	
	else:
		print(color.cyan + "\r\n------ (sum'n dun goofed!) -------\r\n" + color.white)
		sys.exit(1)

	
	
	### do teh closing
	do_teh_closing(loadtest_dir, newprojectid)


	
######################################
## register the project
def registernewproject():
	## run registerchangelog and get the ne projectID and then add to env vars
	print(color.cyan + "\r\n------ (SPECIAL REG NEW PROJECT (2)) -------\r\n" + color.white)
	
	regnewprojcmd = "liquibase registerchangelog"
	# subprocess.Popen(regnewprojcmd, shell=True)
	
	return "some-new-proj-id99"
	

	
######################################
## just a little closer
def do_teh_closing(loadtest_dir, newprojectid):
	## first stop h2
	print(color.magenta + "begin teh_end...(hold each other)..." + color.white)
	print("\r")
		
	## then present the good news!
	print(color.magenta + "------------------------------------------" + color.white)
	print("\r")
	print(color.cyan + " -- Registerchangelog to new project: " +str(loadtest_dir))
	print("\r")
	print(color.cyan + " -- with PROJECTID: " +str(newprojectid) + color.white)
	print("\r")
	print(color.cyan + " -- ps. i love you. boop.boop." + color.white)
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






	
	
	
	