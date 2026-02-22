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


cdm_path = "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/Purchase/Parties.cdm.json"
print(dbutils.fs.head(cdm_path))

# COMMAND ----------


columns = [
    "PartyId",
    "PartyName",
    "LastProcessedChange_DateTime",
    "DataLakeModified_DateTime",
    "PartyAddressCode",
    "EstablishedDate",
    "PartyEmailId",
    "PartyContactNumber",
    "RecordId",
    "TaxId"
]

data_path = "abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/raw_data/Table/Purchase/Parties/"

df_raw = (spark.read.format("csv")
    .option("header", "false")        
    .option("quote", "\"")            
    .option("escape", "\"")
    .option("inferSchema", "true")    
    .load(data_path))

if len(columns) == len(df_raw.columns):
    df_final = df_raw.toDF(*columns)
    print("Finished")
    display(df_final)
else:
    print(f"Wrong")
    display(df_raw)
