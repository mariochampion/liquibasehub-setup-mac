# This README covers two topics:
1. Getting Liquibase Hub and a compatible CLI core app running locally using Docker
2. Using a related python script (soon to be interactive app) to quickly generate changelogs and changesets for load testing


## To use setup-hub-mac.sh 
**Requires** 

 1. docker installed and active: https://docs.docker.com/docker-for-mac/install/
 2. permissions to the right liquibase repos for git clone to work

**Usage**
1. download the .sh file to where you want to create a new directory containing Hub
2. open terminal, cd to file
3. run `sh setup-hub-mac.sh`
4. you will be asked for the liquibase hub branch 
5. you will need to provide a name for a new directory to contain the code
6. you will enter [yes] or [no] to choose --build or not in `docker-compose up`
7. you will enter [yes] or [no] to download the core OSS/PRO app 


## To use makechangelogs.py
**Requires** 

 1. Python installed
 
    -- This script used the older 2.7 as it still the default which ships with MacOs
    
    -- but you might could use Python 3, but i didnt test it: https://docs.python-guide.org/starting/install3/osx/
    
 2. You need to sign up with Liquibase Hub to get an API Key, and you will need to register a changelog to a Hub Project, so you can use the changelogid
 
    -- http://hub.liquibase.com

    -- see docs for details on the new Hub-specific command `liquibase registerchangelog` which connects a changelog's operations to a project stored in your 
    Liquibase Hub account
    
 3. Know how to add and export environment variables to your bash_profile, so you do not put your APIKEY in source control
 
    -- https://www.schrodinger.com/kb/1842
    
    -- quick example of what i added to my bash_profile
    
    `# liquibase env vars and shortcuts`
    
     `export LIQUIBASE_HUB_APIKEY="<put your api key here>"`
     
	 `export LIQUIBASE_HUB_URL="<put a url here>"`
	 
 	 `export LIQUIBASE_HUB_CHANGELOGID="<addyourchangelogid>"`
 	 
 4. Liquibase installed and on your PATH if you want to utilize the optional 3rd parameter of `update`
	 
	 
**Intention** 
	 
The goal of the makechangelogs.py script is that you run updates against a local h2 with and without sending to hub and compare the times logged in the total_time.csv created in the dir which was created to store you testing chaggelogs. for example, run

`python makechangelogs.py 2 100 update`

then run 

`python makechangelogs.py 2 100 update realtime`

and compare the total_times.csv in each timestamped directory.
	 
	 
**Usage** 
1. open terminal and cd into your desired directory
2. `git clone https://github.com/mariochampion/liquibasehub-setup-mac.git`
3. `cd liquibasehub-setup-mac`
4. there are two REQUIRED and two OPTIONAL parameters available in the command line
    1. REQ: number of changelogs to create
    2. REQ: number of changesets in each changelog
    3. OPT: command to run (right now limited to `update`)
    4. OPT: switch to send data to Hub or not [off|realtime]
5. Example: `python makechangelogs.py 5 25 <update> <realtime>` 
6. Output with NO optional `update` parameter: 
	1. a new directory "loadtest_5x25_<HrMinSecTimestamp>" with contents
	2. 5 changelogs named "changelog001.h2.sql", "changelog002.h2.sql", etc with 25 changesets in each
	3. 5 matching liquibase.properties files "liquibase-01.properties", "liquibase-02.properties"
7. Output with optional `update` parameter
	1. same as above BUT then `liquibase update` is called for each properties file
	2. if the optional 3rd parameter is supplied, you will be asked to Enter [y]/[n] if you want to send the commands report to Hub
8. If 4th param is "off" no data sent to Hub. If "realtime" then command metadata and sql content will sent to Hub
9. Also a time tracking changelog01-worktime.csv.CSV, etc file is created to log performance of each changelog file and 
10. A time_total.csv is added which provides total elapsed time in seconds to perform all the commands across all changelogs

**NOTE**
This script used an included H2 database, which is automatically started around line 313 (look for a subprocess.Popen).
If you dont want this, please comment out this line.

	
**NEXT STEPs**
1. DONE -- Add capability to cycle thru the liquibase.properties with liquibase command update
2. DONE -- Create a log file to track timestamps to understand load impacts with and without hub connections as well as is it better to run, for example, 10 changelogs of 1000 changesets, 100 changelogs of 100 changesets, 1 changelog of 10000 changesets, etc.
3. DONE - Add a .csv for total time with number of actions and per action so no need to merge multiple docs, but keep multiple docs 

4. DONE -- Add a hub.mode switch as 4th parameter

4a. DONE - make interactive ask for command and hub.mode if not there

4b. DONE - Use hub,mode to send or not to hub, to get time differences

5. DONE - Add some color to console easier to read

6. Make liquibase.properties interactive to allow non-H2 and remote DBs, etc.

7. DONE - total_time.csv is inaccurate!! it is the actually just the last batch. need to store start outside the loop.

8. REQUIRES HUB API WORK -  actually register each changelog so hub data is more accurate. wont change times, as each changelog has same changesets, so less important.




LICENSES
This repo when cloned contains unmodified binary redistributions for
H2 database engine (https://h2database.com/),
which is dual licensed and available under the MPL 2.0
(Mozilla Public License) or under the EPL 1.0 (Eclipse Public License).
An original copy of the license agreement can be found at:
https://h2database.com/html/license.html
	