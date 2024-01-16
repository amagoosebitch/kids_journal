locals {
  api_gateway_name = "dobry-mir-api-gateway"
}

resource "yandex_api_gateway" "dobry_mir_api_gateway" {
  name      = local.api_gateway_name
  folder_id = local.folder_id
  spec      = file("../web/back/src/openapi.yaml")
}

output "dobry_mir_api_gateway_domain" {
  value = "https://${yandex_api_gateway.dobry_mir_api_gateway.domain}"
}
