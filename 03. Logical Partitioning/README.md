# Logical Partitioning
## Introduction
[Logical Partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/create-and-manage-tabular-model-partitions?view=asallproducts-allversions) is important feature of Power BI which help in improving the refresh time of Power Bi datasets. In this report we will showcase and compare how Logical Partitioning will allow a faster & reliable refresh of new data simply because with partitions you can divide the table data into logical parts that can be managed & refreshed individually. You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.

## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.
- Logical Partition only works with Power Bi Premium subscription


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
3. Create a slicer visual with columns :RegionName (From **region_DQ** table) and Card visual with  Sum of Total_Price(From **orders_DQ** table).
   
#### 2.2.1 Query Analysis : Performance Analyzer and DBSQl 

As shown in screenshot of the Performance Analyzer below the Direct Query takes **953 ms** for Slicer and **946 ms** for aggregate function in card visual  ![Data Source Connection](./images/DirectQuery/PerformanceAnalyzer.png)

You can also find the query execution time by looking at query history in DBSQL . Since both the dimension(Filter visual) and the fact (Card visual) are using Direct Query there are 2 queries fired in the backend also the I/O stats shows 1 row getting read based on the slicer value selected  : 
![Data Source Connection](./images/DirectQuery/QueryHistory.png)

![Data Source Connection](./images/DirectQuery/QueryStats.png)

### 2.2 Import Query Report 
1. Click **Optimize**>**Performance Analyzer** in Power BI desktop.
2. In the Performance Analyzer tab click "**Start Recording**".
3. Create a slicer visual with columns :RegionName (From **region_Import** table) and card visual with Sum of Total_Price(From **orders_Import** table).
   
#### 2.2.1 Query Analysis : Performance Analyzer and DBSQl 

As shown in screenshot of the Performance Analyzer below the Import Query takes only **93 ms** for Slicer as the dimension is using Import method but it takes  **2529 ms** for aggregate function in card visual  ![Data Source Connection](./images/Import/PerformanceAnalyzer.png)

You can also find the query execution time by looking at query history in DBSQL . Since the dimension(Filter visual) is using import method there is no query fired in DBSQL . However the fact (Card visual) is using Direct Query , hence there is only 1 query fired in the backend.  
![Data Source Connection](./images/Import/QueryHistory.png)
As I/O stats shows,in this method **~500k** rows are read and returned . The data is then filtered from Power BI.This is the reason Direct Query method is faster than Import method  : 
![Data Source Connection](./images/Import/QueryStats.png)

### 2.3 Dual Query Report 
1. Click **Optimize**>**Performance Analyzer** in Power BI desktop.
2. In the Performance Analyzer tab click "**Start Recording**".
3. Create a slicer visual with columns :RegionName (From **region_Dual** table) and card visual with Sum of Total_Price(From **orders_Dual** table).
   
#### 2.3.1 Query Analysis : Performance Analyzer and DBSQl 

As shown in screenshot of the Performance Analyzer below the Dual Query takes only **56 ms** for Slicer and takes  **805 ms** for aggregate function in card visual  ![Data Source Connection](./images/Dual/PerformanceAnalyzer.png)

You can also find the query execution time by looking at query history in DBSQL.As Dual Query uses best of Import and Direct Query mode , there is no query fired in DBSQL for dimension(Filter visual) but the fact (Card visual) has it's query fired in backend.  
![Data Source Connection](./images/Dual/QueryHistory.png)
As I/O stats shows,in this method only **1** row is read and returned becasue the filter from slicer visual is passed to the query of Card visual . As Dual Query mode uses best features of Import and Direct mode it is faster than both Direct Query and Import.  
![Data Source Connection](./images/Dual/QueryStats.png)

## Power BI Template 

To automate the process and ease the deployment process save the report as Power BI template. A sample Power BI template [DirectQuery-Dual-Import.pbit](./DirectQuery-Dual-Import.pbit) is already present in the current folder pointing to  **samples** catalog and **TPCH** tables. When you open the template enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL warehouse. The template will create three different reports using Direct Query , Import Query and Dual Query.You can then follow secion 2.2 and 2.3 above to do performance analysis between the reports. 
