# Connecting Databricks to Power BI using Parameters

This guide explains how to set up parameters in Power BI for connecting to Databricks. Utilizing parameters allows for flexibility when connecting to different Databricks workspaces or updating authentication tokens. Follow the steps below to configure the parameters. Also guide shows how to create a Power Bi Template to help automate connecting DBSQL to Power BI 

## Prerequisites

Before you begin, ensure you have the following:

- [Databricks account](https://databricks.com/) and access to a Databricks workspace and also have DBSQL warehouse set up 
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed on your machine.

## Step-by-Step Instructions

### 1. Databricks URL Parameter

1. Open Power BI Desktop.
2. Go to "Home" > "Manage Parameters."
3. Click on "New" to create a new parameter named `ServerHostname`.
4. Set the data type to "Any."
5. Enter the default value as the URL of your Databricks workspace.

![Screenshot 2023-11-13 at 5 11 51 PM](https://github.com/yati1002/PowerBi-Demo/assets/127162962/913676ca-c8ff-431e-87aa-020673d47d97)


### 2. Databricks Token Parameter

1. Create another parameter named `DatabricksToken` for the authentication token.
2. Set the data type to "Text."
3. Do not enter a default value; we will input the token dynamically.

### 3. Data Source Connection

1. Go to "Home" > "Get Data" > "More..."
2. Search for "Databricks" and select "Azure Databricks."
3. Enter the following values:
   - Server: `DatabricksURL`
   - HTTP Path: "/sql/protocolv1/o/<organization-name>/databricks-connector"
   - HTTP Request: "POST"
   - Authentication: "Bearer Token"
   - Token: `DatabricksToken`

   Replace `<organization-name>` with your actual Databricks organization name.

### 4. Dynamic Token Input

1. Create a new query using the "Advanced Editor" and enter the following M code:

   ```m
   let
       Token = Text.FromBinary(Extension.Contents("DatabricksToken")),
   in
       Token
