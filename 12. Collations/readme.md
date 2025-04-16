# Collations
## Introduction
When using BI tools, such as Power BI, users often need filter data. Apart from drop-down lists or slicers, advanced filtering using arbitrary string filters is quite popular among Power BI users.

Until recently implementing case-insensitive filters was a challenge for Databricks users. ```ABC``` and ```abc``` were considered as different strings by Databricks SQL engine. Therefore, either users had to provide exact filter strings, i.e. including upper/lower case, or developers had to implement certain tricks, such as creating additional lower case specifically for filtering.

In this quickstart sample we will showcase the benefits of [Collations](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-collation) when implementing case-insensitive data filtering in Power BI.


## Pre-requisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/), access to a Databricks workspace, and Databricks SQL Warehouse. 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine. Latest version is highly recommended.

  
## Step by Step Instructions
1. Copy-paste the code from [Collations.sql](./Collations.sql) SQL-script to Databricks SQL Editor and execute the script to create the objects required for this example. This includes **powerbisamples** catalog, **tpch** schema, as well as tables and views.
   
2. Open Power BI Desktop, create a new report.
   
3. Connect to Databricks SQL Warehouse, **powerbisamples** catalog, **tpch** schema, and add the following tables to the semantic model
    - **customer_lcase** → Direct Query.
      
4. Create a table visual, add **c_mktsegment** and **c_custkey** columns, configure the latter to use Count aggregation.
    
    ![Table visual](./images/Table.PNG)

7. Add **c_mktsegment** column to Filters, configure it to use Advanced filtering and *contains* filter. 
   
    ![Filter](./images/Filter.PNG)

8. Specify value ```MACH``` (upper case) and Apply filter.

    ![Filtered Table](./images/FilteredTable.PNG)

8. Specify value ```mach``` (lower case) and Apply filter.

    ![Filtered Table](./images/FilteredTable.PNG)

## Conclusion
As we saw in this example, now by leveraging a ```LCASE``` collation for table columns in Unity Catalog we can achieve proper data filtering in Power BI when using **DirectQuery** mode. When using ```LCASE``` collation Databricks SQL converts strings to lower case when comparing strings, hence string becomes case insensitive.

Previously case-insensitive filtering in Power BI required additional tricks, e.g. creating additional columns containing values in upper or lower case only. Now case-insensitive data filtering in Power BI is possible without additional tricks when using Databricks thanks to [Collations](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-collation).


## Power BI Template 

A sample Power BI template [Collations.pbit](./Collations.pbit) is available in the current folder. When opening the template, enter respective **ServerHostname** and **HTTP Path** values of your Databricks SQL Warehouse. The template uses **samples** catalog as well as the name of **Catalog** (default *powerbisamples*) and **Schema** (default *tpch*).
