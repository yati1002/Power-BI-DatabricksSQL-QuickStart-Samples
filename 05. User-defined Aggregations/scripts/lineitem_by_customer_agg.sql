create or replace table lineitem_by_customer_agg
as 
select
  `n_nationkey`,
  min(`l_shipdate`) as `EarliestShipdate`,
  sum(`l_discount`) as `SumofDiscount`,
  sum(`l_quantity`) as `SumOfQuantity`
from
  `samples`.`tpch`.`lineitem` 
    inner join `samples`.`tpch`.`orders` on `l_orderkey` = `o_orderkey`
    inner join `samples`.`tpch`.`customer` on `o_custkey` = `c_custkey`
    inner join `samples`.`tpch`.`nation` on `c_nationkey` = `n_nationkey`
group by
  `n_nationkey`;