drop table if exists poligon.tdr;
drop table if exists poligon.payment;

create schema if not exists poligon
  authorization dwh_worker;

create table poligon.tdr (
  report_date_id          NUMERIC,
  order_date              DATE,
  source_group_id         NUMERIC,
  service_date            DATE,
  device                  VARCHAR(30),
  detail                  VARCHAR(30),
  service_count           NUMERIC,
  service_count1          NUMERIC,
  service_count2          NUMERIC,
  service_count3          NUMERIC,
  town_id                 NUMERIC(3),
  device_group_id         NUMERIC,
  abonent_id              NUMERIC,
  debit                   NUMERIC default 0,
  tdr_group_id            NUMERIC,
  bill_type_id            NUMERIC,
  dbill_type_id           NUMERIC,
  detail_type_id          NUMERIC,
  service_count_group_id  NUMERIC,
  abonent_group_id        NUMERIC,
  date_factor_type_id     NUMERIC,
  factor_type_id          NUMERIC,
  nds_type_id             NUMERIC,
  tariff_type_id          NUMERIC,
  discount_type_id        NUMERIC
)