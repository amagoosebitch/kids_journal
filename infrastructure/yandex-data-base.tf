locals {
  database_name = "dobry-mir-database"
}

resource "yandex_ydb_database_serverless" "dobry-mir-database" {
  name      = local.database_name
  folder_id = local.folder_id
}

output "dobry-mir-database_document_api_endpoint" {
  value = yandex_ydb_database_serverless.dobry-mir-database.document_api_endpoint
}

output "dobry-mir-database_path" {
  value = yandex_ydb_database_serverless.dobry-mir-database.database_path
}
