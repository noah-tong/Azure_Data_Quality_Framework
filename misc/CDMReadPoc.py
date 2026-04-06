# Databricks notebook source
# MAGIC %run ./ADLS_oauth

# COMMAND ----------

df = (spark.read.format("csv")
 .option("path", "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/Purchase/Parties/")
 .load())
display(df)

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="pandascope",key="ClientSecret")
appid = dbutils.secrets.get(scope="pandascope",key="appid")
tenantid = dbutils.secrets.get(scope="pandascope",key="tenantid")



# COMMAND ----------

import json

def get_cdm_columns(cdm_file_path, entity_name):
    
    try:
        
        json_content = dbutils.fs.head(cdm_file_path)
        data = json.loads(json_content)
        
        
        for definition in data.get("definitions", []):
            if definition.get("entityName") == entity_name:
                
                attributes = definition.get("hasAttributes", [])
                cols = [attr.get("name") for attr in attributes]
                return cols
        
        print(f"cant find {entity_name}")
        return None
    except Exception as e:
        print(f"analyze JSON wrong: {e}")
        return None

cdm_path = "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/Purchase/Parties.cdm.json"
data_path = "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/Purchase/Parties/"


auto_columns = get_cdm_columns(cdm_path, "Parties")

if auto_columns:
    print(f"total {len(auto_columns)} columns")
    

    df_raw = (spark.read.format("csv")
        .option("header", "false")
        .option("quote", "\"")
        .option("escape", "\"")
        .option("inferSchema", "true")
        .load(data_path))
    
    if len(auto_columns) == len(df_raw.columns):
        df_final = df_raw.toDF(*auto_columns)
        display(df_final)
    else:
        print(f"match failed: there are {len(auto_columns)} columns in cdm, {len(df_raw.columns)} columns in csv file")
        display(df_raw)
