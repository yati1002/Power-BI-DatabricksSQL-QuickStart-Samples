# Generated vs Persisted dimension
## Introduction
Dimensions play a very big role in data modelling . In Power BI you can either use DAX within PowerBI to Generate dimension table or you can Persist dimension in the source system . Carefully selecting the method to generate these dimensions are really important because report latency and end user experience may be impacted if a report generates multiple SQL-queries. Hence it's important to build efficient semantic models in Power BI by leveraging both Databricks SQL and Power BI capabilities wisely. 
In the present quickstart sample we will showcase the benefits of Persisted dimension over Generated dimension by using example of date dimension . Persisted dimension helps generate fewer SQL-queries, hence achieving overall better performance and user experience.


## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/), access to a Databricks workspace, and Databricks SQL Warehouse. 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine. Latest version is highly recommended.


  
## Step by Step Instructions
1. Copy-paste the code from [GeneratedvsPersisted.sql](./Generated%20vs%20Persisted%20dimension.sql) SQL-script to Databricks SQL Editor and execute the script to create the objects required for this example. This includes **powerbisamples** catalog, **tpch** schema, as well as tables.
2. Open Power BI Desktop, create a new report.
3. Connect to Databricks SQL Warehouse, **powerbisamples** catalog, **tpch** schema, and add the following tables from  to the semantic model
    - orders -> Direct Query 
    - dim_date -> Dual Mode
4. Create a Generated date dimension table from **orders** table by running the below DAX. This geenrated table contains the dates based on Min and Max Orderdate,
  ```
    date_generated = 
VAR StartDate = CALCULATE(MIN('orders'[o_orderdate]))
VAR EndDate = CALCULATE(MAX('orders'[o_orderdate]))
RETURN 
    ADDCOLUMNS(
        CALENDAR(StartDate,EndDate)
        , "Year", YEAR([Date])
        , "Month", MONTH([Date])
        , "Day", DAY([Date])
        , "Quarter", QUARTER([Date])
    )
 ```
5. Configure table relationships as shown on the picture below.
![Data model](./images/DataModel.PNG)
7. In **orders** table create 3 calculated measures using the following DAX-formulas. These measures calculate the number of orders where an order item is delivered in Large, Medium, or Small bag.
    ```
    CountOrdersLargeBag = CALCULATE(COUNT(orders[o_orderkey]), 'part'[p_container]="LG BAG")
    CountOrdersMediumBag = CALCULATE(COUNT(orders[o_orderkey]), 'part'[p_container]="MED BAG")
    CountOrdersSmallBag = CALCULATE(COUNT(orders[o_orderkey]), 'part'[p_container]="SM BAG")
    ```
8. Create a table visual and add **region.r_name** column, as well as prevously created measures **CountOrdersLargeBag**, **CountOrdersMediumBag**, and **CountOrdersSmallBag**. Turn off Totals for the table visual.
![Table visual](./images/TableVisual1.PNG)
9. Refresh visuals using [Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer) in Power BI Desktop.
10. Check the number of SQL-queries in Databricks Query History. You should see 3 SQL-queries, each calculating one of the measures used in the table visual.
![Query History](./images/QueryHistory1.PNG) 
The reason why Power BI generated 3 SQL-queries is that the measures use related table **part** to filter data. Therefore, Power BI is not able to combine these 3 queries into a single one.

11. Next we will be using **orders_transformed** view which for every order item identifies the type of bag.  
    ``` sql
    create or replace view powerbisamples.tpch.orders_transformed as
    select o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority
        , max(if(p_container='SM BAG', 1, 0)) as sm_bag
        , max(if(p_container='MED BAG', 1, 0)) as med_bag
        , max(if(p_container='LG BAG', 1, 0)) as lg_bag
    from powerbisamples.tpch.orders
        join powerbisamples.tpch.lineitem on o_orderkey=l_orderkey
        join powerbisamples.tpch.part on l_partkey=p_partkey
    group by all;
    ```

12. In Power BI semantic model in **orders_transformed** table create 3 calculated measures using the following DAX-formulas. These measures produce the same results as original measures.
    ```
    CountOrdersLargeBag_v2 = SUM(orders_transformed[lg_bag])
    CountOrdersMediumBag_v2 = SUM(orders_transformed[med_bag])
    CountOrdersSmallBag_v2 = SUM(orders_transformed[sm_bag])
    ```
13. Create a table visual and add **region.r_name** column, as well as prevously created measures **CountOrdersLargeBag_v2**, **CountOrdersMediumBag_v2**, and **CountOrdersSmallBag_v2**. Turn off Totals for the table visual.
![Table visual](./images/TableVisual2.PNG)
14. Refresh visuals using [Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer) in Power BI Desktop.

15. Check the number of SQL-queries in Databricks Query History. You should see only 1 SQL-queries.
![Query History](./images/QueryHistory2.PNG) 
The reason why Power BI generated only 1 SQL-queries in this case is that the measures use SUM aggregation function over columns in the same table **orders_transformed**. Therefore, Power BI could use as single SQL-query.

## Conclusion
...

## Power BI Template 

A sample Power BI template [Generate vs Persisted dimension.pbit](./Generated%20vs%20Persisted%20dimension.pbit) is present in the current folder. When opening the template, enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL Warehouse. The template uses **samples** catalog, therefore you don't need to prepare any additional data for this report.

