# Connecting Power BI to Databricks SQL Using Parameters

## Introduction
There are instances when data analyts have to connect to different Databricks SQL environment or a different Databricks SQL instances. This can be a lot of manual work and can often lead to errors. This guide explains how to we can automate the process of connecting Databricks SQL by using parameters in Power BI . Utilizing parameters allows for flexibility when connecting to different Databricks workspaces or connecting to a different Databricks SQL instance. To create a parametrized report you can follow the steps mentioned in the [Step by Step Instructions](#step-by-step-instructions) section 

## Prerequisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.

# Step by Step Instructions

### 1. Databricks Connection Parameter

1. Open Power BI Desktop.
2. Go to **"Home"** > "**Manage Parameters**."
3. Click on **"New"** to create a new parameter named `ServerHostname`.
4. Set the data type to "**Any."**
5. Enter the default value as the URL of your Databricks workspace.

Repeat the abpve Process and create Parameter for HTTP path from SQL warehouse. You can get the HTTP Path from DBSQL Warehouse Connection Details. It should start with "/sql/1.0" .
Your parameters should look like below : 
![Screenshot 2023-11-13 at 5 11 51 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/913676ca-c8ff-431e-87aa-020673d47d97)




### 2. Data Source Connection

1. Go to **"Home" **> **"Get Data"** > **"More..."**
2. Search for "Databricks" and select "Azure Databricks."
3. Enter the following values:
   - Server: `ServerHostname`
   - HTTP Path: Enter the HTTP path copied fro DBSQL Warehouse Connection detail tab

![Screenshot 2023-11-13 at 6 29 48 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/260f1d00-fe69-49d6-80f9-82748db95061)


### 3. Add Parameters to M Query
1. Go to "Transform Data">Open Query Editor > On the Query Setting Click on Source
2. In the M Query under Databricks.Catalog replace HostName and HTTP Path with the parameters created in Step 1
   
![Screenshot 2023-11-13 at 7 09 20 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/76de44a4-3139-4faa-b4ec-1332b6835a38)

## Power BI Template 

To Automate the process and ease the deployment process save the report as Power Bi Template . A sample Power BI template(PBI-DB-Connection.pbit)  is already present in PBI Template folder pointing to Customer Table in Sample Catalog.   . When you open the template enter ServerHostname and HTTP Path value based on your Databricks ServerHostName and HTTP Path for DBSQL ,  a default Customer Table poiniting to  Customer Table in Sample Catalog is created . You can then add your respective catalog and tables and create report
![Screenshot 2023-11-13 at 7 16 53 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/f4f0d804-6e6e-402d-84a3-874443ea36be)

![Screenshot 2023-11-13 at 7 21 20 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/92d799e5-af52-4aa9-8a6d-e939373ace2e)


