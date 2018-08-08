#!/bin/bash

sudo sudo su -
usermod -aG wheel vagrant
exit
su - vagrant

yum install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
yum install postgresql10
yum install postgresql10-server
/usr/pgsql-10/bin/postgresql-10-setup initdb
systemctl enable postgresql-10
systemctl start postgresql-10

cd /home/share
sudo yum localinstall oracle* --nogpgcheck