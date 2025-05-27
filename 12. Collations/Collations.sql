create catalog if not exists powerbisamples;
create schema if not exists powerbisamples.tpch;

create or replace table powerbisamples.tpch.customer_lcase (
  c_custkey bigint,
  c_name string,
  c_address string,
  c_nationkey string,
  c_phone string,
  c_acctbal decimal(18,2),
  c_mktsegment string COLLATE UTF8_LCASE,
  c_comment string);

insert into powerbisamples.tpch.customer_lcase
select * from samples.tpch.customer;
