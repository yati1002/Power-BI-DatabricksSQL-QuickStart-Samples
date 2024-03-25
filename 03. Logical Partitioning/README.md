# Logical Partitioning
## Introduction
[Logical Partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/create-and-manage-tabular-model-partitions?view=asallproducts-allversions) is important feature of Power BI which help in improving the refresh time of Power Bi datasets. In this report we will showcase and compare how Logical Partitioning will allow a faster & reliable refresh of new data simply because with partitions you can divide the table data into logical parts that can be managed & refreshed individually. You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.

## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.
- Power BI **Premium** workspace
- DAX Studio
- Tabular Editor
  
## Step by Step Instructions
1.We have an initial Power BI dataset which is based on **samples** catalog, **tpch** schema. There is only one fact table **orders** which is set to Import mode.
2.Next we created a copy of the orders table and renamed it as **orders-non-partitioned**. The Create [non partitioned table script](./Create-non-partitioned-table.xmla) is also avaiable in this repo . As shown below you can use DAX Studio to view the default partitions 
(/01.%20Connecting%20Power%20BI%20to%20Databricks%20SQL%20using%20Parameters)

## Power BI Template 

To automate the process and ease the deployment process save the report as Power BI template. A sample Power BI template [DirectQuery-Dual-Import.pbit](./DirectQuery-Dual-Import.pbit) is already present in the current folder pointing to  **samples** catalog and **TPCH** tables. When you open the template enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL warehouse. The template will create three different reports using Direct Query , Import Query and Dual Query.You can then follow secion 2.2 and 2.3 above to do performance analysis between the reports. 
