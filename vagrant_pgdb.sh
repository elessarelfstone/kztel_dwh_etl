#!/bin/bash

sudo yum install mc -y

# posgtres installlation
sudo yum install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm -y
sudo yum install postgresql10 -y
sudo yum install postgresql10-server -y
/usr/pgsql-10/bin/postgresql-10-setup initdb
sudo systemctl enable postgresql-10
sudo systemctl start postgresql-10
sudo adduser dwh_worker
echo pass | passwd dwh_worker --stdin
sed -i 's/^local/#local/' /var/lib/pgsql/10/data/pg_hba.conf
sed -i 's/^host/#host/' /var/lib/pgsql/10/data/pg_hba.conf
echo "local 	all		all		trust" >> /var/lib/pgsql/10/data/pg_hba.conf
echo "host 	all		all		192.168.100.1/16			md5" >> /var/lib/pgsql/10/data/pg_hba.conf
echo "listen_addresses = '*'" >> /var/lib/pgsql/10/data/postgresql.conf
sudo systemctl reload postgresql-10
psql -U postgres -d postgres -a -w -f /vagrant/db/system.sql
psql -U dwh_worker -d dwh -a -w -f /vagrant/db/sys_migration_1.sql

#oracle client installation
cd /home/share
sudo yum localinstall oracle* --nogpgcheck -y
sudo echo "export ORACLE_HOME=/usr/lib/oracle/12.2/client64" >> /home/vagrant/.bash_profile
sudo echo "export PATH=$ORACLE_HOME/bin:$PATH" >> /home/vagrant/.bash_profile
sudo echo "export LD_LIBRARY_PATH=$ORACLE_HOME/lib" >> /home/vagrant/.bash_profile
sudo echo "export TNS_ADMIN=$ORACLE_HOME/network/admin" >> /home/vagrant/.bash_profile
sudo echo "export NLS_LANG=AMERICAN_AMERICA.AL32UTF8" >> /home/vagrant/.bash_profile
source /home/vagrant/.bash_profile