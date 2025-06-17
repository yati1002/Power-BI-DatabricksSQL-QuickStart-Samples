# Power BI on Databricks SQL - QuickStart Samples

## Introduction
This repo contains the samples demonstrating the usage of [Power BI](https://powerbi.microsoft.com/) with [Databricks SQL](https://www.databricks.com/product/databricks-sql). The objective of these samples is to demonstrate reference implementation and some of the best practices using Power BI with Databricks SQL.

For quick access to [this repository](.) and [Best Practices Cheat Sheet](https://www.databricks.com/sites/default/files/2025-04/2025-04-power-bi-on-databricks-best-practices-cheat-sheet.pdf) please use the QR-code below. 👇


| QuickStart Samples repo | Best Practices Cheat Sheet |
| ------ | ----------- |
| <p align="center"> <img width="35%" src="./images/qrcode-repo.png" /> </p> | <p align="center"> <img width="30%" src="./images/qrcode-cheatsheet.png" /> </p> |

## Table of Contents

| #    | Folder | Description |
| ---- | ------ | ----------- |
| 00   | [Best Practices Cheat Sheet](00.%20Best%20Practices%20Cheat%20Sheet/)    | Power BI on Databricks Best Practices Cheat Sheet    |
| 01   | [Connection Parameters](01.%20Connection%20Parameters/)    | Using Power BI parameters to efficiently manage connections to Databricks SQL    |
| 02   | [DirectQuery-Dual-Import](./02.%20DirectQuery-Dual-Import/)    | Using different storage modes - Direct Query vs Dual vs Import    |
| 03   | [Logical Partitionoing](./03.%20Logical%20Partitioning/)    | Improving data refresh performance with Power BI partitioning    |
| 04   | [Query Parallelisation](./04.%20Query%20Parallelization/)    | Improving performance of Power BI Reports in Direct Query mode using query parallelisation    |
| 05   | [User-defined aggregations](./05.%20User-defined%20aggregations/)    | Improving performance of Power BI reports using User-defined aggregations    |
| 06   | [Dynamic M Query Parameters](./06.%20Dynamic%20M%20Query%20Parameters/)    |  Using Dynamic M Query Parameters for better control over SQL-query generation and performance optimization   |
| 07   | [Query optimization using PK](./07.%20Query%20optimization%20using%20PK/)    |  Query optimization using primary key constraints   |
| 08   | [Automatic aggregations](./08.%20Automatic%20aggregations/)    |  Improving performance of Power BI reports using Automatic aggregations   |
| 09   | [Private Connections](./09.%20Private%20Connections/)    |  Making private connections to the Databricks Workspace from the Power BI Service   |
| 10   | [Pushdown Calculations](10.%20Pushdown%20Calculations/)    |  Improve performance of DirectQuery and Composite models by pushing calculations down to Databricks SQL  |
| 11   | [Generated vs Persisted dimensions](./11.%20Generated%20vs%20Persisted%20dimension/)    |  Improve performance of DirectQuery and Composite models by using generated vs persisted dimension tables  |
| 12   | [Collations](./12.%20Collations/)    |  Using Collations for case-insensitive search and filtering  |