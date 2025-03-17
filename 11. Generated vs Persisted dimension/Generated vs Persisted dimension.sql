create catalog if not exists powerbisamples;
create schema if not exists powerbisamples.tpch;

create or replace table powerbisamples.tpch.orders as select * from samples.tpch.orders;

create or replace table powerbisamples.tpch.dim_date as
select distinct
  o_orderdate as date,
  year(o_orderdate) as year,
  month(o_orderdate) as month,
  day(o_orderdate) as day,
  dayofweek(o_orderdate) as day_of_week,
  weekofyear(o_orderdate) as week_of_year,
  quarter(o_orderdate) as quarter
from powerbisamples.tpch.orders;

