#!/bin/bash
set -x

echo "`(cat version.json) | jq '.version = .version + 1'`"  > version.json;

app_version=$(jq -r '.version' version.json);

docker build -t ${DOBRY_MIR_API_REPOSITORY_NAME}:0.0.$app_version . ;

docker push ${DOBRY_MIR_API_REPOSITORY_NAME}:0.0.$app_version;

yc sls container revisions deploy \
	--folder-id ${FOLDER_ID} \
	--container-id ${ANEKDOT_API_CONTAINER_ID} \
	--memory 512M \
	--cores 1 \
	--execution-timeout 5s \
	--concurrency 8 \
	--environment AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID},AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY},DOCUMENT_API_ENDPOINT=${DOCUMENT_API_ENDPOINT},APP_VERSION=$app_version,YDB_ENDPOINT=grpcs://ydb.serverless.yandexcloud.net:2135,YDB_DATABASE=/ru-central1/b1ge6sseudpphs9ug20c/etntllofdu9tcsl3rki1  \
	--service-account-id ${API_SA_ID} \
	--image "${DOBRY_MIR_API_REPOSITORY_NAME}:0.0.$app_version";
