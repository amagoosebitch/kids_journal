#!/bin/sh
set -x
terraform apply -target=yandex_ydb_database_serverless.dobry-mir-database
terraform apply -target=yandex_iam_service_account.dobry_mir_api_sa
terraform apply -target=yandex_container_registry.default
terraform apply -target=yandex_container_repository.dobry-mir-api_repository
yc container registry configure-docker
yc sls container create --name dobry-mir-api-container --folder-id ${FOLDER_ID}
terraform output -raw aws_private_key > aws_private_key
