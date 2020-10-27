#!/bin/bash

export FIWARE_SERVICE="demoservice"
export FIWARE_SERVICEPATH="/demo/path"
export type=robot
export id=robot01

# register service
curl -i "http://localhost:4041/iot/services/" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
     -H "Content-Type: application/json" \
     -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "${type}",
      "cbroker": "http://orion:1026",
      "resource": "/iot/json",
      "entity_type": "${type}"
    }
  ]
}
__EOS__

# retrieve service
curl -sS "http://localhost:4041/iot/services/" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"

# register device
curl -i "http://localhost:4041/iot/devices/" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
     -H "Content-Type: application/json" \
     -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "${id}",
      "entity_name": "${id}",
      "entity_type": "${type}",
      "timezone": "Asia/Tokyo",
      "protocol": "json",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        },
        {
          "name": "mode",
          "type": "string"
        },
        {
          "name": "errors",
          "type": "array"
        },
        {
          "name": "pose",
          "type": "object"
        },
        {
          "name": "destination",
          "type": "object"
        },
        {
          "name": "accuracy",
          "type": "object"
        },
        {
          "name": "battery",
          "type": "object"
        },
        {
          "name": "metadata",
          "type": "object"
        },
        {
          "name": "image",
          "type": "object"
        }
      ],
      "commands": [
        {
          "name": "naviCmd",
          "type": "command"
        }
      ],
      "transport": "HTTP",
      "endpoint": "http://amqp10-converter:3000/amqp10/cmd/${type}/${id}"
    }
  ]
}
__EOS__


# retrieve device
curl -sS "http://localhost:4041/iot/devices/${id}" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"

curl -sS "http://localhost:1026/v2/entities/${id}?type=${type}" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"
