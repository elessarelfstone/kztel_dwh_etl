-- DDL
drop table if exists sys.data_source;
drop table if exists sys.data_source_table;
drop table if exists sys.data_source_type;
drop sequence if exists sys.data_source_seq;
drop sequence if exists sys.data_source_table_seq;
drop sequence if exists sys.data_source_type_seq;

create schema if not exists sys
  authorization dwh_worker;


create sequence sys.data_source_seq
  increment 1
  minvalue 1;

create sequence sys.data_source_table_seq
  increment 1
  minvalue 1;

create sequence sys.data_source_type_seq
  increment 1
  minvalue 1;


create table sys.data_source_type (
  data_source_type_id INT4         not null,
  name                VARCHAR(500) null,
  code                VARCHAR(100) null,
  tables              JSONB        null,
  constraint pk_data_source_type primary key (data_source_type_id),
  constraint data_src_type_code unique (code)
);

create table sys.data_source (
  data_source_id      INT4         not null,
  data_source_type_id INT4         not null,
  name                VARCHAR(500) not null,
  conn_detail         JSONB        not null,
  tns                 VARCHAR(500) not null,
  code                VARCHAR(100) not null,
  constraint pk_data_source primary key (data_source_id),
  constraint data_src_code unique (code)
);

create table sys.data_source_table (
  data_source_table_id INT4         not null,
  data_source_type_id  INT4         not null,
  name                 VARCHAR(100) not null,
  description          TEXT         null,
  code                 VARCHAR(100) not null,
  script_template      VARCHAR(100) null,
  constraint pk_data_source_table primary key (data_source_table_id),
  constraint data_src_tb_code unique (code)
);


alter table sys.data_source
  add constraint fk_data_src_type_ds foreign key (data_source_type_id)
references sys.data_source_type (data_source_type_id);

alter table sys.data_source_table
  add constraint fk_data_src_type_dst foreign key (data_source_type_id)
references sys.data_source_type (data_source_type_id);

-- DML

insert into sys.data_source_type
(data_source_type_id, name, code, tables)
values (1, 'Автоматизированная система расчетов АСР БИТТл', 'ASR', '{}');

-----


insert into sys.data_source
(data_source_id, data_source_type_id, name, conn_detail, tns, code)
values (2, 1, 'АСР БИТТЛ АКТОБЕ', '{
  "db_sid": "AKTOASR",
  "db_host": "10.71.200.8",
  "db_pass": "ciuyrhvv",
  "db_port": "1521",
  "db_user": "reporter"
}',
        '(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=10.71.200.8)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=aktoasr.Aktobe)))',
        'asr_aktobe');

insert into sys.data_source
(data_source_id, data_source_type_id, name, conn_detail, tns, code)
values (1, 1, 'АСР БИТТЛ ЗКО', '{
  "db_sid": "URALASR",
  "db_host": "10.71.200.15",
  "db_pass": "ciuyrhvv",
  "db_port": "1521",
  "db_user": "reporter"
}',
        '(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=10.71.200.15)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=URALASR.weskaz)))',
        'asr_uralsk');

insert into sys.data_source
(data_source_id, data_source_type_id, name, conn_detail, tns, code)
values (1, 1, 'АСР БИТТЛ Алматы', '{
  "db_sid": "ORCL1",
  "db_host": "10.10.70.63",
  "db_pass": "ciuyrhvv",
  "db_port": "1521",
  "db_user": "reporter"
}',
        '(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=10.10.70.63)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=orcl1)))',
        'asr_almaty');

insert into sys.data_source
(data_source_id, data_source_type_id, name, conn_detail, tns, code)
values (1, 1, 'АСР БИТТЛ Астана', '{
  "db_sid": "ORCL",
  "db_host": "10.72.1.50",
  "db_pass": "ciuyrhvv",
  "db_port": "1521",
  "db_user": "reporter"
}',
        '(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL=TCP)(HOST=10.72.1.50)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=orcl.Astanatelecom)))',
        'asr_astana');


-----


insert into sys.data_source_table
(data_source_table_id, data_source_type_id, name, description, code, script_template)
values (1, 1, 'poligon.tdr', '', 'tdr', 'tdr.sqtmpl');

insert into sys.data_source_table
(data_source_table_id, data_source_type_id, name, description, code, script_template)
values (2, 1, 'poligon.payment', '', 'payment', 'payment.sqtmpl');

