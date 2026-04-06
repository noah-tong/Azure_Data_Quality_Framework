terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.67.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "imported_rg" {
  name     = "dq_dev"
  location = "Germany West Central" 
}


resource "azurerm_data_factory" "adf" {
  name                = "dq-dev-adf"
  resource_group_name = azurerm_resource_group.imported_rg.name
  location            = azurerm_resource_group.imported_rg.location
}


resource "azurerm_mssql_server" "sql_server" {
  name                         = "dqdevsqldbsv"
  resource_group_name          = azurerm_resource_group.imported_rg.name
  location                     = azurerm_resource_group.imported_rg.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_user     
  administrator_login_password = var.sql_admin_password 
}


resource "azurerm_mssql_database" "dq_db" {
  name      = "dq_dev_sqldb"
  server_id = azurerm_mssql_server.sql_server.id
  sku_name  = "Basic" 
}


resource "azurerm_databricks_workspace" "adb" {
  name                = "dq-dev-adb"
  resource_group_name = azurerm_resource_group.imported_rg.name
  location            = azurerm_resource_group.imported_rg.location
  sku                 = "standard"
}


resource "azurerm_key_vault" "kv" {
  name                = "dq-dev-kvault"
  resource_group_name = azurerm_resource_group.imported_rg.name
  location            = azurerm_resource_group.imported_rg.location
  tenant_id           = var.tenant_id
  sku_name            = "standard"
}


resource "azurerm_storage_account" "adls" {
  name                     = "dqdevadls"
  resource_group_name      = azurerm_resource_group.imported_rg.name
  location                 = azurerm_resource_group.imported_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true 
}