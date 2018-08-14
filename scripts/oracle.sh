#!/bin/bash

cd /home/share
sudo yum localinstall oracle* --nogpgcheck -y
sudo echo "export ORACLE_HOME=/usr/lib/oracle/12.2/client64" >> /home/vagrant/.bash_profile
sudo echo "export PATH=$ORACLE_HOME/bin:$PATH" >> /home/vagrant/.bash_profile
sudo echo "export LD_LIBRARY_PATH=$ORACLE_HOME/lib" >> /home/vagrant/.bash_profile
sudo echo "export TNS_ADMIN=$ORACLE_HOME/network/admin" >> /home/vagrant/.bash_profile
sudo echo "export NLS_LANG=AMERICAN_AMERICA.AL32UTF8" >> /home/vagrant/.bash_profile
source /home/vagrant/.bash_profile