create catalog if not exists powerbisamples;
create schema if not exists powerbisamples.tpch;

create or replace table powerbisamples.tpch.region as select * from samples.tpch.region;
create or replace table powerbisamples.tpch.nation as select * from samples.tpch.nation;
create or replace table powerbisamples.tpch.customer as select * from samples.tpch.customer;
create or replace table powerbisamples.tpch.part as select * from samples.tpch.part;
create or replace table powerbisamples.tpch.orders as select * from samples.tpch.orders;
create or replace table powerbisamples.tpch.lineitem as select * from samples.tpch.lineitem;

create or replace view powerbisamples.tpch.orders_transformed as
select o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority
    , max(if(p_container='SM BAG', 1, 0)) as sm_bag
    , max(if(p_container='MED BAG', 1, 0)) as med_bag
    , max(if(p_container='LG BAG', 1, 0)) as lg_bag
from powerbisamples.tpch.orders
    join powerbisamples.tpch.lineitem on o_orderkey=l_orderkey
    join powerbisamples.tpch.part on l_partkey=p_partkey
group by all;