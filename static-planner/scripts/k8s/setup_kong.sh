#!/bin/bash

. ./.env

SERVICE_NAME="static-planner-service"
BACKEND_URL="http://static-route-planner:3000"
ROUTE_NAME="static-planner-route"
CONSUMER_NAME="static-planner-consumer"

# delete existing objedcts
echo "# delete existing objects"
consumerId=$(curl -s "http://kong-gateway:8001/consumers/" | jq -r ".data[] | select(.username == \"${CONSUMER_NAME}\") | .id")
curl -s "http://kong-gateway:8001/consumers/${consumerId}" -X DELETE
pluginIds=($(curl -s "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins" | jq -r ".data[].id"))
for id in ${pluginIds[@]}; do
  curl -s "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins/${id}" -X DELETE
done

curl -s "http://kong-gateway:8001/services/${SERVICE_NAME}/routes/${ROUTE_NAME}" -X DELETE
curl -s "http://kong-gateway:8001/services/${SERVICE_NAME}" -X DELETE
echo ""

# create service
echo "# create service: ${SERVICE_NAME}"
curl -i "http://kong-gateway:8001/services" -X POST \
     --data "name=${SERVICE_NAME}" \
     --data "url=${BACKEND_URL}"
echo ""

# create route
echo "# create route: ${ROUTE_NAME}"
curl -i "http://kong-gateway:8001/services/${SERVICE_NAME}/routes" -X POST \
     --data "name=${ROUTE_NAME}" \
     --data "hosts[]=${ROUTING_HOST}" \
     --data "protocols[]=https"
echo ""

# set key-auth
echo "# set key-auth"
curl -i "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins" -X POST \
     --data "name=key-auth" \
     --data "config.key_names[]=authorization" \
     --data "config.hide_credentials=true"
curl -i "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins" -X POST \
     --data "name=acl" \
     --data "config.whitelist[]=${ROUTE_NAME}"
curl -i "http://kong-gateway:8001/consumers" -X POST \
     --data "username=${CONSUMER_NAME}" \
     --data "custom_id=${CONSUMER_NAME}"
curl -i "http://kong-gateway:8001/consumers/${CONSUMER_NAME}/key-auth" -X POST \
     --data "key=${CONSUMER_KEY}"
curl -i "http://kong-gateway:8001/consumers/${CONSUMER_NAME}/acls" -X POST \
     --data "group=${ROUTE_NAME}"

