# Using storage modes - DirectQuery vs Dual vs Import

## Introduction
[Storage Modes](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-storage-mode) are really important aspect of Power BI. Whether you're a seasoned Power BI user or just getting started, understanding storage modes is crucial for maximizing performance and efficiently managing your data. This Read Me file serves as your roadmap, providing insights into the various storage modes offered by Power BI . In this report we will showcase and compare performance between Direct Query , Import and Dual storage mode and show how dual helps with performance of the report. You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.

## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.


## Step by Step Instructions

## 1. Databricks Data Source Connection 

1. Open Power BI Desktop
2. Go to **"Home"**> **"Get Data"** > **"More..."**
3. Search for **"Databricks"** and select **"Azure Databricks"** (or **"Databricks"** when using Databricks on AWS or GCP).
4. Enter the following values:
   - **Server Hostname**: Enter the Server hostname value from Databricks SQL Warehouse connection details tab.
   - **HTTP Path**: Enter the HTTP path value  from Databricks SQL Warehouse connection details tab.

Below is the sample screenshot of how the data source would look like

![Data Source Connection](./images/conneciton.png)


## Best Practice 
It is always a good practice to parameterize your connection string. This really helps ease out the development expeience as you can dynamically connect to any DBSQL warehouse. For details on how to paramterize your connection string you can refer to [this](/01.%20Connecting%20Power%20BI%20to%20Databricks%20SQL%20using%20Parameters) article.

## 2. Showcasing perfromance with storage modes for dimension table
In the next section we will compare different storage modes and showcase which storage mode is good for dimension table.There are two common query patterns generated against Dimension tables : 1. Using query slicer/filter  , 2.Aggregation on the Fact table using data in the dimension table.  For our testing scenario we are using a "**Small**" Pro cluster and we will create report with both query pattterns highlighted above. 
### 2.1 Data Model Creation
To make performance testing easy to follow we will use "Samples" catalog and "TPCH" schema and ingest below tables. In order to compare the performance between three modes we will ingest dimension table with different storage modes and analyze time taken based on each mode.

1.region_DQ:Region dimension table ingested with storage mode as Direct Query.

2.nation_DQ:Nation dimension table containing nation name and details ingested with storage mode as Direct Query.

3.customer_DQ:Customer dimesntion table containg customer details ingested with storage mode as Direct Query.

4.region_Dual:Region dimension table ingested with storage mode as Dual. 

5.nation_Dual:Nation dimension table containing nation name and details ingested with storage mode as Dual.

6.customer_Dual:Customer dimesntion table containg customer details ingested with storage mode as Dual.

7.region_Import:Region dimension table ingested with storage mode as Import. 

8.nation_Import:Nation dimension table containing nation name and details ingested with storage mode as Import.

9.customer_Import:Customer dimesntion table containg customer details ingested with storage mode as Import.

10.orders_DQ:Orders fact table ingestd with storage mode as Direct Quary.

Below is the screen shot of how our star schema data model and the report with 2 dimension scenario's mentioned above looks like:

![Data Source Connection](./images/DataModel.png)

### 2.2 Direct Query Report 
In order to get best results it and avoid caching it's better to run the test against warm up warehouse by running few queries against warehouse. After warehouse is warmed up follow below steps :
1. Click **Optimize**>**Performance Analyzer** in Power BI desktop.
2. In the Performance Analyzer tab click "**Start Recording**".
3. Create a slicer visual with columns :RegionName (From **region_DQ** table), Sum of Total_Price(From **orders_DQ** table).
   
#### 2.2.1 Query Analysis : Performance Analyzer and DBSQl 

As shown in screenshot of the Performance Analyzer below the Direct Query takes **953 ms** for Slicer and **946 ms** for aggregate function in card visual  ![Data Source Connection](./images/DirectQuery/PerformanceAnalyzer.png)

You can also find the query execution time by looking at query history in DBSQL . Since both the dimension(Filter visual) and the fact (Card visual) are using Direct Query there are 2 queries fired in the backend also the I/O stats shows 1 row getting read : 
![Data Source Connection](./images/DirectQuery/QueryHistory.png)

![Data Source Connection](./images/DirectQuery/QueryStats.png)

### 2.2 Import Query Report 
1. Click **Optimize**>**Performance Analyzer** in Power BI desktop.
2. In the Performance Analyzer tab click "**Start Recording**".
3. Create a slicer visual with columns :RegionName (From **region_Import** table), Sum of Total_Price(From **orders_DQ** table).
   
#### 2.2.1 Query Analysis : Performance Analyzer and DBSQl 

As shown in screenshot of the Performance Analyzer below the Import Query takes only **93 ms** for Slicer as the dimension is using Import method but it takes  **2529 ms** for aggregate function in card visual  ![Data Source Connection](./images/Import/PerformanceAnalyzer.png)

You can also find the query execution time by looking at query history in DBSQL . Since the dimension(Filter visual) is using import method and the fact (Card visual) is using Direct Query there is only 1 query fired in the backend. Also the I/O stats shows 1 row getting read : 
![Data Source Connection](./images/DirectQuery/QueryHistory.png)

![Data Source Connection](./images/DirectQuery/QueryStats.png)

## Power BI Template 

To automate the process and ease the deployment process save the report as Power BI template. A sample Power BI template [Managed_Aggregate_Template.pbit](./PBIX/Managed_Aggregate_Template.pbit) is already present in the current folder pointing to  **samples** catalog and **TPCH** tables.Please run [Aggregate_tbl_create](./Scripts/Aggregate_tbl_create) DDL script to create table in HMS before running the PowerBI template. Once done when you open the template enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL warehouse. The template will create a warmup report (to warm up warehouse),DirectQuery report using Nation and LineItem table and Aggregate_Table report using Nation and LineItem_Agg table.You can then follow secion 2.2 and 2.3 above to do performance analysis between both the reports. 
