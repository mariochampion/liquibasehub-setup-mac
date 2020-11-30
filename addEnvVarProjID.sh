## ===================================================================
# FOR MAC OS USERS ONLY (i think)
# this quick script will add an env var to your bash_profile
# which is used by the registerchangelog portion of the companion makechangelog.py
# for convenience, add an alias to your bash_profile, like:
# alias addprojid='sh addEnvVarProjID.sh'
# and then run in terminal:
# $>addprojid <pasteyourProjectIDhere>
# and this will add the echo line below to the end of your bash profile
#
# thanks and always remember: this robot loves you. 
# boop boop!
## ===================================================================


NEWPROJID=$1
echo 'export LIQUIBASE_HUB_PROJECTID="'$NEWPROJID'"' >> $HOME/.bash_profile
