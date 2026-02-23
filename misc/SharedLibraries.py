# Databricks notebook source
import pyspark.sql.functions as F 
import datetime
import pandas as pd
import dateutil

# COMMAND ----------

ADLS_DEV_BASE_PATH = "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/"
DELTALAKE_RAW_PATH = "DeltaLake/Raw/"

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="pandascope",key="ClientSecret")
appid = dbutils.secrets.get(scope="pandascope",key="appid")
tenantid = dbutils.secrets.get(scope="pandascope",key="tenantid")

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="pandascope",key="ClientSecret")
appid = dbutils.secrets.get(scope="pandascope",key="appid")
tenantid = dbutils.secrets.get(scope="pandascope",key="tenantid")

service_credential = dbutils.secrets.get(scope="pandascope",key="ClientSecret")
appid = dbutils.secrets.get(scope="pandascope",key="appid")
tenantid = dbutils.secrets.get(scope="pandascope",key="tenantid")

spark.conf.set("fs.azure.account.auth.type.dqdevadls.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.dqdevadls.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.dqdevadls.dfs.core.windows.net", appid)
spark.conf.set("fs.azure.account.oauth2.client.secret.dqdevadls.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.dqdevadls.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenantid}/oauth2/token")

# COMMAND ----------

import json

def readEntity(manifestPath, entity):
  
    base_path = f"abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/{manifestPath}"
    cdm_file_path = f"{base_path}/{entity}.cdm.json"
    data_folder_path = f"{base_path}/{entity}/"
    
    try:
  
        json_content = dbutils.fs.head(cdm_file_path)
        data = json.loads(json_content)
        
        cols = None
        for definition in data.get("definitions", []):
            if definition.get("entityName") == entity:
                attributes = definition.get("hasAttributes", [])
                cols = [attr.get("name") for attr in attributes]
                break
        
        if not cols:
            print(f"cant find {entity}")
            return None

        df_raw = (spark.read.format("csv")
            .option("header", "false")
            .option("quote", "\"")
            .option("escape", "\"")
            .option("inferSchema", "true")
            .load(data_folder_path))
        
    
        if len(cols) == len(df_raw.columns):
            df_final = df_raw.toDF(*cols)
            return df_final
        else:
            print(f"match failed: there are {len(cols)} columns in cdm, {len(df_raw.columns)} columns in csv file")
            return df_raw
            
    except Exception as e:
        print(f"analyze JSON wrong: {e}")
        return None
    


# COMMAND ----------

def writeRawToDeltaLake(entityDf,deltaLakePath):
    entityDf.write.mode("overwrite").option("overwriteSchema","True").option("path",ADLS_DEV_BASE_PATH + deltaLakePath).save()

# COMMAND ----------

def readFromDeltaPath(entityName):
    df = (spark.read.format("delta")
      .option("path",f"{ADLS_DEV_BASE_PATH}/{DELTALAKE_RAW_PATH}{entityName}")
      .load()
      )
    return df


# COMMAND ----------

def saveDeltaTableToCatalog(df,schema,tableName):
    schema = schema.lower()
    tableName = tableName.lower()
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    df.write.format("delta").mode("overwrite").saveAsTable(f"{schema}.{tableName}")


# COMMAND ----------


