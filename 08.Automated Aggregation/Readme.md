# Automatic Aggregation
## Introduction
[Automatic Aggregation](https://learn.microsoft.com/en-us/power-bi/enterprise/aggregations-auto) in Power BI use state-of-the-art machine learning (ML) to continuously optimize DirectQuery semantic models for maximum report query performance. Automatic aggregations are built on top of existing user-defined aggregations infrastructure first introduced with composite models for Power BI. In this example we will showcase how to enable Automatic Aggregation on Power Bi report and train Automatic Aggregation in order to speed up exploring report . You can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section.

## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/), access to a Databricks workspace, and Databricks SQL Warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.
- Power BI **Premium** workspace

  
## Step by Step Instructions
1. We have an initial Power BI dataset which is based on **samples** catalog, **tpch** schema. All the dimension tables **customer** and **nation** are set up as Dual storage mode . The fact table  **orders** and **lineitem** are set to Direct Query mode. Below is the datamodel for the sample report 
3. Publish this report to a **Premium** workspace.
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

