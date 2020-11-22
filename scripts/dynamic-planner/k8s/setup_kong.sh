#!/bin/bash

. ./.env
. ./../../kong/k8s/.env

SERVICE_NAME="dynamic-planner-service"
BACKEND_URL="http://dynamic-route-planner:3000"
ROUTE_NAME="dynamic-planner-route"

# delete existing objedcts
echo "# delete existing objects"
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
     --data "hosts[]=${DYNAMIC_PLANNER_DOMAIN}" \
     --data "protocols[]=https"
echo ""

# set plugins
echo "# set plugins"
curl -i "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins" -X POST \
     --data "name=basic-auth" \
     --data "config.hide_credentials=true"
curl -i "http://kong-gateway:8001/routes/${ROUTE_NAME}/plugins" -X POST \
     --data "name=acl" \
     --data "config.whitelist[]=${BASIC_CONSUMER}"

