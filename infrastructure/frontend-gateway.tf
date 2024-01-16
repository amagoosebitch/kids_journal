locals {
  website_gateway_name = "dobry-mir-frontend-gateway"
}

resource "yandex_api_gateway" "dobry_mir_frontend_gateway" {
  name      = local.website_gateway_name
  folder_id = local.folder_id
  spec      = file("../web/front/kids-journal/openapi.yaml")
}

output "dobry_mir_frontend_gateway_domain" {
  value = "https://${yandex_api_gateway.dobry_mir_frontend_gateway.domain}"
}
