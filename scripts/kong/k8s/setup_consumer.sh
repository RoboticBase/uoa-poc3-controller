#!/bin/bash

. ./.env

# delete existing objedcts
echo "# delete existing objects"
consumerIds=($(curl -s "http://kong-gateway:8001/consumers/" | jq -r ".data[].id"))
for id in ${consumerIds[@]}; do
  curl -s "http://kong-gateway:8001/consumers/${id}" -X DELETE
done
echo ""

# create consumers
echo "# create key-consumer"
curl -i "http://kong-gateway:8001/consumers" -X POST \
     --data "username=${KEY_CONSUMER}" \
     --data "custom_id=${KEY_CONSUMER}"
curl -i "http://kong-gateway:8001/consumers/${KEY_CONSUMER}/acls" -X POST \
     --data "group=${KEY_CONSUMER}"
curl -i "http://kong-gateway:8001/consumers/${KEY_CONSUMER}/key-auth" -X POST \
     --data "key=${KEY_CONSUMER_KEY}"
echo ""

echo "# create basic-consumer"
curl -i "http://kong-gateway:8001/consumers" -X POST \
     --data "username=${BASIC_CONSUMER}" \
     --data "custom_id=${BASIC_CONSUMER}"
curl -i "http://kong-gateway:8001/consumers/${BASIC_CONSUMER}/acls" -X POST \
     --data "group=${BASIC_CONSUMER}"
curl -i "http://kong-gateway:8001/consumers/${BASIC_CONSUMER}/basic-auth" -X POST \
     --data "username=${BASIC_CONSUMER_USERNAME}" \
     --data "password=${BASIC_CONSUMER_PASSWORD}"
echo ""

