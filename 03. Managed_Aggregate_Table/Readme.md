# Improving Performance of Power BI Reports using Aggregation Table

## Introduction
[Aggregation tables](https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced) are the unsung heroes of Power BI, quietly optimizing performance and efficiency behind the scenes. In the dynamic world of data analysis, where speed and accuracy are paramount, these specialized tables play a crucial role in improving performance for large Power BI dataset in DirectQuery storage mode. This guide explains how we can set up Aggregation tables and also showcases how Aggregation tables help improve perfromance over Power BI dataset. You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.

## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.


## Step by Step Instructions

### 1. Databricks Data Source Connection 

1. Open Power BI Desktop
2. Go to **"Home"**> **"Get Data"** > **"More..."**
3. Search for **"Databricks"** and select **"Azure Databricks"** (or **"Databricks"** when using Databricks on AWS or GCP).
4. Enter the following values:
   - **Server Hostname**: Enter the Server hostname value from Databricks SQL Warehouse connection details tab.
   - **HTTP Path**: Enter the HTTP path value  from Databricks SQL Warehouse connection details tab.

Below is the sample screenshot of how the data source would look like

![Data Source Connection](./ScreenShots/03.png)


## Best Practice 
It is always a good practice to parameterize your connection string. This really helps ease out the development expeience as you can dynamically connect to any DBSQL warehouse. For details on how to paramterize your connection string you can refer to ![this](/01.%20Connecting%20Power%20BI%20to%20Databricks%20SQL%20using%20Parameters) article.


## Power BI Template 

To automate the process and ease the deployment process save the report as Power BI template. A sample Power BI template [DBSQL-Parameterized-Connection.pbit](DBSQL-Parameterized-Connection.pbit) is already present in the current folder pointing to **customer** table in **samples** catalog. When you open the template enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL warehouse, a default report poiniting to **customer** table in **samples** catalog is created. You can then add your respective catalog and tables and create report.
![Template connection](./images/05.png)

![Sample report](./images/06.png)




