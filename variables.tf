variable "sql_admin_user" {
  type    = string
  default = "sqladmin"
}

variable "sql_admin_password" {
  type      = string
  sensitive = true
}

variable "tenant_id" {
  type = string
}