#!/bin/sh
echo "Download MAC OS Installer from github.com/liquibase/liquibase/releases"
echo "1) give us liquibase version wont ya?"
read LBV

cd ~/Documents/liquibase/liquibase-apps/
curl -LJO https://github.com/liquibase/liquibase/releases/download/v${LBV}/liquibase-macos-installer-${LBV}.dmg
open liquibase-macos-installer-${LBV}.dmg
