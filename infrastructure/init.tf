terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = local.token
  cloud_id  = local.cloud_id
  folder_id = local.folder_id
  zone      = local.zone
}


locals {
  token     = "y0_AgAAAAA_rdRtAATuwQAAAADZ4PBxCglhTH4TTvKFSnA5ieDXvbGGfeg"
  cloud_id  = "b1ge6sseudpphs9ug20c"
  folder_id = "b1gf54qrjkrq75uriq7l"
  zone      = "ru-central1-a"
}
