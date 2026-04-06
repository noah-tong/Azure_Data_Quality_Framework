# Databricks notebook source
dbutils.secrets.listScopes()

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="pandascope",key="ClientSecret")
appid = dbutils.secrets.get(scope="pandascope",key="appid")
tenantid = dbutils.secrets.get(scope="pandascope",key="tenantid")

# COMMAND ----------

# DBTITLE 1,Untitled
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

display(dbutils.fs.ls("abfss://oaonoperationsdev@dqdevadls.dfs.core.windows.net/"))

# COMMAND ----------


