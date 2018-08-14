create database dwh;
create user dwh_worker with encrypted password 'dwh';
alter user dwh_worker with superuser;
grant all privileges on database dwh to dwh_worker;
\c dwh