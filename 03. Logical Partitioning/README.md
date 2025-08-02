# Logical Partitioning
## Introduction
[Logical Partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/create-and-manage-tabular-model-partitions?view=asallproducts-allversions) is an important feature of Power BI which helps improving the refresh time of Power BI semantic models. In this example we will showcase and compare how Logical Partitioning can provide a faster data refresh by enabling parallel processing of multiple partitions. You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.



## Prerequisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/), access to a Databricks workspace, Unity Catalog, and Databricks SQL Warehouse
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/), latest version is highly recommended
- Power BI **Premium** workspace
- [Tabular Editor](https://tabulareditor.com/), free version is sufficient
- [DAX Studio](https://daxstudio.org/)
- [SQL Server Management Studio](https://aka.ms/ssmsfullsetup)

  

## Step by step walkthrough

1. We have an initial Power BI dataset which is based on **samples** catalog, **tpch** schema. There is only one table **orders** which is set to Import mode.
2. Publish this report to a **Premium** workspace.
2. Next, we connect to XMLA-endpoint of the published dataset using [SQL Server Management Studio](https://aka.ms/ssmsfullsetup) and create a non-partitioned version of **orders** table - **orders-non-partitioned** - by executing [Create-non-partitioned-table.xmla](./Create-non-partitioned-table.xmla) script.
As shown below you can use [DAX Studio](https://daxstudio.org/) to see that the table consists of a single partition: ![Non partitioned table](./images/Nonpartitioned.png)
3. Next, we create another version of **orders** table - **orders-partitioned** - using [Create-partitioned-table.xmla](./Create-partitioned-table.xmla) script.
 Alternatively, you can use [Tabular Editor](https://tabulareditor.com/) to create partitions. [This](https://www.youtube.com/watch?v=6CRqdsLjHNA) video demonstrates how you can create parititons. In our example we have created these partitions based on the **o_priority** column which results in even data distribution. As shown below in DAX Studio screenshot, 5 parittions are created in **orders-partitioned** table and every partition contains ~1.5M records:
![Partitioned table](./images/Partitioned.png)
4. To showcase the benefits of partioning we process both the **orders-partitioned** and **orders-non-partitioned** tables using [SQL Server Management Studio](https://aka.ms/ssmsfullsetup). As shown below, it took **8min25sec** to process non-paritioned table. Whereas the processing of parititioned table took just under **4min** for the same total number of records. 
   
**orders-non-partitioned**
![Processing orders-non-partitioned table](./images/03.png)

**orders-partitioned**
![Processing orders-non-partitioned](./images/04.png)

## Conclusion
When using **Import** mode in Power BI, configuring partitions for large tables may significantly improve overall table processing performance. While for a non-partitioned table Power BI uses a single thread and ingests and compresses data as a single chunk, for a partitioned table Power BI uses multiple threads where each thread ingests and compresses own chunk of data. Therefore, end-to-end table processing is much faster.
As we saw above in our case the performance gain was **~50%**. For bigger tables the performance gain can be even higher.

## Power BI Template 

A sample Power BI template [Logical-Partitioning.pbit](./Logical-Partitioning.pbit) is present in the current folder. When opening the template, enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL Warehouse. The template uses **samples** catalog, therefore you don't need to prepare any additional data for this report.
