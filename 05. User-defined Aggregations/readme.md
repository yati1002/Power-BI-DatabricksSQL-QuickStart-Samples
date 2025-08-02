# User-defined Aggregations
 
## Introduction

[User-defined aggregations](https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced) are a powerful - yet often overlooked - tool for optimizing query performance, especially when working with large *DirectQuery* semantic models. By configuring specialized aggregation tables within your data model, you enable Power BI to automatically serve commonly requested summaries from in-memory cache rather than querying the backend source each time. This not only delivers faster and more responsive reports but also reduces the workload on source systems, making your analytics solutions more scalable and efficient.

In this quickstart, you’ll learn how to set up [User-defined aggregations](https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced) and see first-hand how they can significantly boost the performance of your Power BI semantic models.


## Prerequisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/), access to a Databricks workspace, Unity Catalog, and Databricks SQL Warehouse
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/), latest version is highly recommended



## Step by step walkthrough

### 1. Data Model

1. Create a catalog and a schema in Databricks Unity Catalog.
    ```sql
    CREATE CATALOG IF NOT EXISTS powerbiquickstarts;
    USE CATALOG powerbiquickstarts;
    CREATE SCHEMA IF NOT EXISTS tpch;
    USE SCHEMA tpch;
    ```

2. Create test tables in the catalog by replicating tables from **`samples`** catalog.
    ```sql
   CREATE OR REPLACE TABLE nation AS SELECT * FROM samples.tpch.nation;
   CREATE OR REPLACE TABLE customer AS SELECT * FROM samples.tpch.customer;
   CREATE OR REPLACE TABLE orders AS SELECT * FROM samples.tpch.orders;
   CREATE OR REPLACE TABLE lineitem AS SELECT * FROM samples.tpch.lineitem;

   CREATE OR REPLACE TABLE lineitem_by_nation_agg AS
   SELECT
   `n_nationkey`
   , min(`l_shipdate`) as `EarliestShipdate`
   , sum(`l_discount`) as `SumofDiscount`
   , sum(`l_quantity`) as `SumOfQuantity`
   FROM `samples`.`tpch`.`lineitem` 
      INNER JOIN `samples`.`tpch`.`orders` on `l_orderkey` = `o_orderkey`
      INNER JOIN `samples`.`tpch`.`customer` on `o_custkey` = `c_custkey`
      INNER JOIN `samples`.`tpch`.`nation` on `c_nationkey` = `n_nationkey`
   GROUP BY ALL;
    ```

1. Open Power BI Desktop → **"Home"** → **"Get Data"** → **"More..."**.

2. Search for **Databricks** and select **Azure Databricks** (or **Databricks** when using Databricks on AWS or GCP).

3. Enter the following values:
   - **Server Hostname**: Enter the Server hostname value from Databricks SQL Warehouse connection details tab.
   - **HTTP Path**: Enter the HTTP path value  from Databricks SQL Warehouse connection details tab.

> [!TIP]
> It is always a good practice to parameterize your connections. This really helps ease out the development expeience as you can dynamically connect to any Databricks SQL warehouse. For details on how to paramterize your connection string you can refer to [Connection Parameters](/01.%20Connection%20Parameters/) article.

4. Connect to **`powerbiquickstarts`** catalog, **`tpch`** schema.

5. Add tables to the semantic model as follows.
   - **`customer`** - *Dual* storage mode. Dimension table containing customer information and connected to nation dimension table using nationkey.
   - **`nation`** - *Dual* storage mode. Dimension table containing nation name and details.
   - **`orders`** - *DirectQuery* storage mode. Fact table containing orders information and connected to customer dimension using customerkey.
   - **`lineitem`** - *DirectQuery* storage mode. Fact table containing details like order shipment date, discount price etc. 
   - **`orders_agg`** - *DirectQuery* storage mode. Copy of **`orders`** table and used for aggregate table report.
   - **`lineitem_agg`** - *DirectQuery* storage mode. Copy of **`lineitem`** table and used for aggregate table report.
   - **`lineitem_by_nation_agg`** - *DirectQuery* storage mode. Aggregated **`lineitem`** data.

8. Create table relationships as follows.
   - **`nation`** → **`customer`** → **`orders`** → **`lineitem`** 
   - **`nation`** → **`customer`** → **`orders_agg`** → **`lineitem_agg`** 
   - **`nation`** → **`lineitem_by_nation_agg`**
   
> ![IMPORTANT]
> The relationship between **`nation`** and **`lineitem_by_nation_agg`** must **be One to many (1:*)** with **Single** cross-filter direction.

   The resulting data model should look like on the screenshot below.

   ![Data Model](./images/DataModel-v2.png)


Next, we will analyze the performance of a test report using pure *DirectQuery* mode and *User-defined Aggregation*.


#### 2.2. DirectQuery

1. Create a new report page. Add a Table visual. Add columns to the Table visual as follows.
   - **`n_nation`** from **`nation`** table
   - Sum of **`l_discount`** from **`lineitem`** table
   - Sum of **`l_quantity`** from **`lineitem`** table
   - Earliest **`l_shipdate`** from **`lineitem`** table

2. Open **Optimize** → **Performance Analyzer**.

3. In the Performance Analyzer tab, click **Start Recording** → **Refresh visuals**.

4. Perfomance Analyzer tab will display the Table visual and a DAX query. Click on **Copy Query**. The DAX query should look similar to [Sample DAX Query](./scripts/Sample_DAX_Query.dax) script. Below is the screenshot of Direct Query report page.
   
   <img width="800" src="./images/DirectQueryReport.png" alt="DirectQuery - report" />

5. To compare the performance between *pure DirectQuery* and *User-defined Aggregations*, it is important to get objective and precise query execution times.

6. Open **DAX Studio** and click **Server Timings**.

7. Open the [Sample_DAX_Query.dax](./scripts/Sample_DAX_Query.dax) query or paste DAX-query that was previously copied in Power BI Desktop. Click **Run**. As shown in screenshot below, the query takes **5.7s**.

   <img width="800" src="./images/DirectQueryDAXStudio.png" alt="DirectQuery - DAX Studio" />

9. You can also find the SQL-query execution time by looking at Databricks Query History. As shown below, the query took **~3.7s** and read **~38M** rows. 

   <img width="600" src="./images/DirectQueryExecutionQueryHistory.png" alt="DirectQuery - query profile" />


> [!TIP]
> If you get much better performance, this may be due to results being served from Query Result Cache. To mitigate this, you may recreate test tables by running SQL-statements mentioned above.

   The SQL-query looks as follows. Power BI built a SQL-query joining fact table **`lineitem`** with **`orders`** and **`nation`**.

   ``` sql
   select ...
   from
   (
      select ...
      from
         (
         select ...
         from
            (
               select ...
               from
               (
                  select ...
                  from
                     `powerbiquickstarts`.`tpch`.`lineitem` as `OTBL`
                     inner join `powerbiquickstarts`.`tpch`.`orders` as `ITBL`
                        on (`OTBL`.`l_orderkey` = `ITBL`.`o_orderkey`)
               ) as `OTBL`
                  inner join `powerbiquickstarts`.`tpch`.`customer` as `ITBL`
                     on (`OTBL`.`o_custkey` = `ITBL`.`c_custkey`)
            ) as `OTBL`
               inner join `powerbiquickstarts`.`tpch`.`nation` as `ITBL`
               on (`OTBL`.`c_nationkey` = `ITBL`.`n_nationkey`)
         ) as `ITBL`
      group by
         `n_name`
   ) as `ITBL`
   where ...
   ```


#### 2.3. User-defined Aggregations

1. Switch to Power BI Desktop → **Model view**.

2. Right Click **lineitem_by_nation_agg** → **Manage aggregations**.

3. Configure aggregation table as shown below on the screenshot.

   | Aggregation column | Summarization | Detail table | Detail column |
   | ---------------------- | --- | ------------------ | ---------------- |
   | **`n_nationkey`**      | -   |     -              |        -         |
   | **`EarliestShipdate`** | Min | **`lineitem_agg`** | **`l_shipdate`** |
   | **`SumofDiscount`**    | Sum | **`lineitem_agg`** | **`l_discount`** |
   | **`SumOfQuantity`**    | Sum | **`lineitem_agg`** | **`l_quantity`** |

   <img width="600" src="./images/ManageAggregations-v2.png" alt="Manage aggregations" />

4. Create a new report page. Add a Table visual. Add columns to the Table visual as follows.
   - **`n_nation`** from **`nation`** table
   - Sum of **`l_discount`** from **`lineitem_agg`** table
   - Sum of **`l_quantity`** from **`lineitem_agg`** table
   - Earliest **`l_shipdate`** from **`lineitem_agg`** table

5. Open **Optimize** → **Performance Analyzer**.

6. In the Performance Analyzer tab, click **Start Recording** → **Refresh visuals**.

7. Perfomance Analyzer tab will display the Table visual and a DAX query. Click on **Copy Query**. The DAX query should look similar to [Sample_DAX_Query_Using_Aggregations](./scripts/Sample_DAX_Query_Using_Aggregations.dax) script. Below is the screenshot of **User-defined Aggregation** report page.

   <img width="800" src="./images/AggTableReport.png" alt="Aggregated table - report" />

8. Open **DAX Studio** and click **Server Timings**.

9. Open the [Sample_DAX_Query_Using_Aggregations.dax](./scripts/Sample_DAX_Query_Using_Aggregations.dax) query or paste DAX-query that was previously copied in Power BI Desktop. Click **Run**.

10. As shown in screenshot below the query takes **2.8 sec**.
   <img width="800" src="./images/AggTableDAXStudio.png" alt="Aggregated table - DAX Studio" />


   Also, as shown in the screenshot, the first row under **RewriteAttempted** shows **MatchFound**, i.e., Power BI was able to find the aggregate table for this query. Hence, during the query execution as shown in the screenshot the values are fetched from **`lineitem_by_nation_agg`** instead of **`lineitem_agg`** fact table.

11. You can also find the query execution time by looking at Databricks Query History. As shown below the query took **~2.8s** and read only **50** rows (instead of ~**38M** rows). 

   <img width="600" src="./images/AggTableExecutionQueryHistory.png" alt="Query profile" />

   The SQL-query looks as follows. Power BI built a SQL-query joining fact table **`lineitem`** with **`orders`** and **`nation`**.

   ``` sql
   ```



## Conclusion
As we can see **User-defined Aggregations** tables give performance benefit of ~**50%** over pure Direct Query by reading much less data, **order of magnitude** in our case, from **lineitem_by_nation_agg** as compared to pure Direct Query which reads directly from fact tables.



## Power BI Template 

To automate the process and ease the deployment process save the report as Power BI template. A sample Power BI template [User-Defined-Aggregations.pbit](./User-Defined-Aggregations.pbit) is already present in the current folder pointing to  **samples** catalog and **tpch** schema. Please run [lineitem_by_customer_agg.sql](./scripts/lineitem_by_customer_agg.sql) DDL script to create table in HMS before running opening Power BI template. Once done when you open the template enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL Warehouse. The report will contain **Warmup** report page (to warm up SQL Warehouse), **Direct Query** report page reading from original tables, and **User-defined Aggregations** report page which use aggregation table. You can then follow secion 2.2 and 2.3 above to do performance analysis between both the reports. 


--

A Power BI template [User-defined-Aggregations.pbit](./User-Defined-Aggregations.pbit) and [Collations.sql](./Collations.sql) script are  provided in this folder to demonstrate the usage of Collations outlined above. To use the template, simply enter your Databricks SQL Warehouse's **`ServerHostname`** and **`HttpPath`**, along with the **`Catalog`** and **`Schema`** names that correspond to the environment set up in the instructions above.