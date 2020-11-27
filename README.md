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
4. you will be asked for the liquibase hub branch (you need permissions)
5. you will need to provide a name for a new directory to contain the code
6. you will enter [yes] or [no] to choose --build or not in `docker-compose up`
7. you will enter [yes] or [no] to download the core OSS/PRO app 


## To use makechangelogs.py
**Requires** 

 1. Python installed
 
    -- This script used the older 2.7 as it still the default which ships with MacOs
    
    -- but you might could use Python 3, but i didnt test it: https://docs.python-guide.org/starting/install3/osx/
    
 2. You need to sign up with Liquibase Hub to get an API Key, and you will need to register a changelog to a Hub Project, so you can use the projectID in your ENV vars
 
    -- https://hub.liquibase.com

    -- see docs for details on the new Hub-specific command `liquibase registerchangelog` which connects a changelog's operations to a project stored in your 
    Liquibase Hub account at 
    -- https://docs.liquibase.com/commands/community/registerchangelog.html
    
 3. Know how to add and export environment variables to your bash_profile, so you do not put your APIKEY in source control
 
    -- https://www.schrodinger.com/kb/1842
    
    -- quick example of what i added to my bash_profile
    
    `# liquibase env vars and shortcuts`
    
     `export LIQUIBASE_HUB_APIKEY="<put your api key here>"`
     
	 `export LIQUIBASE_HUB_URL="<put a url here>"` (in 99.9% cases this is https://hub.liquibase.com)
	 
 	 `export LIQUIBASE_HUB_PROJECTID="<put your Hub Project ID>"`
 	 
 4. Liquibase installed and on your PATH if you want to utilize the optional 3rd parameter of `update`
	 
	 
**Intention** 
	 
The goal of the makechangelogs.py script is that you run updates from a formatted SQL(default) changelog file against a local h2 with and without sending to hub and compare the times logged in the total_time.csv created in the dir which was created to store you testing changelogs. for example, run

`python makechangelogs.py 2 100 update`

then run 

`python makechangelogs.py 2 100 update all`

and compare the total_times.csv in each timestamped directories.
	 
	 
**Usage** 
1. open terminal and cd into your desired directory
2. `git clone https://github.com/mariochampion/liquibasehub-setup-mac.git`
3. `cd liquibasehub-setup-mac`

4a. Example usage: `python makechangelogs.py 5 25` to create 5 formatted SQL changelogs of 25 changesets 


4b. Example usage: `python makechangelogs.py 5 25 update all` to create 5 formatted SQL changelogs of 25 changesets, run `update` and send `all` data to Hub using local and transient H2 database


4c. Example usage: `python makechangelogs.py 5 25 update meta` to create 5 formatted SQL changelogs of 25 changesets, run `update` and send only `meta` data to Hub using local and transient H2 database

4d. Example usage: `python makechangelogs.py 5 25 update meta xml` to create 5 XML changelogs of 25 changesets, run `update` and send only `meta` data to Hub using local and transient H2 database

**Details**
1. There are two REQUIRED and two OPTIONAL parameters available in the command line. THE ORDER MATTERS.
    1. REQ: number of changelogs to create
    2. REQ: number of changesets in each changelog
    3. OPT: command to run (right now limited to `update`)
    4. OPT: switch to send data to Hub or not [all=default|meta|off]
2. Example: `python makechangelogs.py 5 25 <update> <all>` 
3. Output with NO optional `update` parameter: 
	1. a new directory "loadtest_5x25_<HrMinSecTimestamp>" with contents
	2. 5 changelogs named "changelog001.h2.sql", "changelog002.h2.sql", etc with 25 changesets in each
	3. 5 matching liquibase.properties files "liquibase-01.properties", "liquibase-02.properties", etc
4. Output with optional `update` parameter: 
	1. same as above BUT then `liquibase update` is called for each properties file
	2. if the optional 3rd parameter is supplied, you will be asked to Enter [y]/[n] if you want to send the commands report to Hub
5. The 4th param details:
    1. "all" reports command's metadata, sql, and log content will sent to Hub
    2. "meta" reoprts only the command's metadata (and no sql or log content) will sent to Hub
    3. "off" reports no data sent to Hub
6. Secret and optional 5th parameter to choose sql or xml changelogfile types! (27 NOV 2020)
	1. Example: `python makechangelogs.py 5 25 <update> <all|off|meta> <xml|sql=default>`
	2. Liquibase formatted SQL changelog files created by default.
	3. JSON and YAML changelog file types coming soon.
7. Time-tracking files:
	1. A time tracking changelog01-worktime.csv.CSV, etc file is created to log performance of each changelog file and 
	2. A time_total.csv is added which provides total elapsed time in seconds to perform all the commands across all changelogs

**NOTE**
This script used an included local in-memory H2 database, which you can [y] or [n] decide to auto-start when running the script via 
`python makechangelogs.py <N> <M>` for interactive setup.

	
**NEXT STEPs**
1. DONE -- Add capability to cycle thru the liquibase.properties with liquibase command update
2. DONE -- Create a log file to track timestamps to understand load impacts with and without hub connections as well as is it better to run, for example, 10 changelogs of 1000 changesets, 100 changelogs of 100 changesets, 1 changelog of 10000 changesets, etc.
3. DONE - Add a .csv for total time with number of actions and per action so no need to merge multiple docs, but keep multiple docs 

4. DONE -- Add a hub.mode switch as 4th parameter

4a. DONE - make interactive ask for command and hub.mode if not there

4b. DONE - Use hub,mode to send or not to hub, to get time differences

5. DONE - Add some color to console easier to read

6. DONE - Make loadtest interactive to allow starting local in-mem H2 db or not

7. DONE - total_time.csv is inaccurate!! it is the actually just the last batch. need to store start outside the loop.

8. DONE - REQUIRES HUB API WORK -  actually register each changelog so hub data is more accurate. wont change times, as each changelog has same changesets, so less important.

9. DONE - add rollback script to tool's SQL changelogs so local users can do rollbacks (outside this tool, for now)

10. DONE - check in on all startup params permutations for the correct follow ups when params missing

11. DONE - enable XML changelogs

12. enable rollback commands via this tool






** LICENSES **

This repo when cloned contains unmodified binary redistributions for
H2 database engine (https://h2database.com/),
which is dual licensed and available under the MPL 2.0
(Mozilla Public License) or under the EPL 1.0 (Eclipse Public License).


An original copy of the license agreement can be found at:
https://h2database.com/html/license.html
	
	
	
ps. i love you. boop.boop.