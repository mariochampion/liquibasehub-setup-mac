#!/bin/sh

BASE_CORE_APP_URL="http://mariochampion.com/liquibase"
CURRENT_CORE_APP="liquibase-4.1"

echo "So you want to run Liquibase Hub on your mac?"
echo "NOTE: You must have docker installed and running!"
echo "(https://docs.docker.com/docker-for-mac/install/)"

echo "1) give us a case-sensitive branch name, like 'DAT-5000':"
read GHUB_BRANCH

echo "2) and a directory to create to put things in:"
read HUBDIR

echo "3) enter [y] for docker to build or [n] to not build docker"
read BUILD_OR_NOT

echo "4) do you want to download the latest core app [y] or [n]"
read GETCORE

echo "5) and finally, start local in-mem H2 database? [y] or [n]"
read STARTH2


echo "\x1B[96mOk, starting setup...\x1B[0m "
echo " "



if [ -d "$HUBDIR" ]; then
  mv $HUBDIR $HUBDIR"-bkup"
fi
mkdir $HUBDIR



if [ "$GETCORE" == "yes" ] || [ "$GETCORE" == "y" ]
then
	ADDEDAPP=" added core app,"
	echo "\x1B[96mDownloading latest core app ("$CURRENT_CORE_APP".zip)\x1B[0m"
	wget $BASE_CORE_APP_URL"/"$CURRENT_CORE_APP".zip"
	unzip $CURRENT_CORE_APP".zip"


	echo "\x1B[96mcore app downloaded and unzipped and now to move it with: \x1B[0m"
	echo "\x1B[96mmv -R $CURRENT_CORE_APP $HUBDIR/$CURRENT_CORE_APP\x1B[0m"
	mv $CURRENT_CORE_APP $HUBDIR/$CURRENT_CORE_APP

	## get rid of some stuff
	rm -r __MACOSX
	rm -r $CURRENT_CORE_APP
	rm $CURRENT_CORE_APP".zip"
fi


echo "\x1B[96mmade a directory, ${ADDEDAPP} gonna cd there and do a git clone\x1B[0m"

cd $HUBDIR
echo " "
echo "-------------------------------"
pwd
ls -all
echo "-------------------------------"
echo " "

git clone https://github.com/Datical/liquibase-hub.git --branch $GHUB_BRANCH --single-branch

echo " "

echo "\x1B[96mgit clone succesful.\x1B[0m"
echo " "

echo "\x1B[96mcd into liquibase-hub\x1B[0m"
cd liquibase-hub
pwd
ls -all
git status


echo "\x1B[96m "
echo "-------------------------------------------------------"
echo " "
echo "                    about to do:                       "
if [ "$BUILD_OR_NOT" == "no" ]
then
	echo "                   docker-compose up                   "
elif [ "$BUILD_OR_NOT" == "yes" ]
then
	echo "             docker-compose down --volumes             "
	echo "              docker-compose up --build                "

else
	echo "             docker-compose down --volumes             "
	echo "              docker-compose up --build                "
fi

echo "             (maybe go get a cup of tea)               "
echo " "
echo "       Access UI from : http://localhost:8888/         "
echo "  Swagger API Docs: http://localhost:8888/swagger-ui   "
echo "-------------------------------------------------------"
echo "\x1B[0m"

if [ "$BUILD_OR_NOT" == "no" ]
then
	docker-compose up
elif [ "$BUILD_OR_NOT" == "yes" ]
then
	docker-compose down --volumes 
	docker-compose up --build
else
	docker-compose down --volumes 
	docker-compose up --build
fi
