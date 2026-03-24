# Data Quality Automation Framework

A metadata-driven framework to automate data validation within a **Medallion Architecture** using **Azure Databricks**, **PySpark**, and **ADF**.

##  Project Overview
* **Objective**: Decouple validation rules from execution code to enable scalable, self-service data governance.
* **Core Logic**: Uses **SQL-based metadata** to drive **PySpark** validation engines.
* **Key Feature**: **Watermark-based incremental auditing** to reduce compute costs and avoid redundant checks.

##  Tech Stack
* **Compute**: Azure Databricks (PySpark)
* **Orchestration**: Azure Data Factory (ADF)
* **Metadata Store**: Azure SQL Database
* **Governance**: Unity Catalog & Delta Lake

##  Project Structure
<img width="1200" height="896" alt="image" src="https://github.com/user-attachments/assets/8c0866d0-2250-4624-a1d3-75757d082baa" />


##  How It Works
1.  **ADF** triggers the workflow and manages the **Watermark**.
2.  **Databricks** fetches active rules from SQL Metadata.
3.  **Spark** executes SQL queries dynamically and isolates **Bad Records**.
4.  **Logic Apps** monitor results to trigger **Azure DevOps** tickets for failed checks.
