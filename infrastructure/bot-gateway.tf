locals {
  bot_gateway_name = "dobry-mir-bot-gateway"
}

resource "yandex_api_gateway" "dobry_mir_bot_gateway" {
  name      = local.bot_gateway_name
  folder_id = local.folder_id
  spec      = file("../web/back/tg_bot/openapi.yaml")
}

output "dobry_mir_bot_gateway_domain" {
  value = "https://${yandex_api_gateway.dobry_mir_bot_gateway.domain}"
}
