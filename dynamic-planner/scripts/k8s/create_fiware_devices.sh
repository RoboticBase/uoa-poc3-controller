#!/bin/bash

export FIWARE_SERVICE="uoapoc2020"
export FIWARE_SERVICEPATH="/"
export type=jadrobot

# register service
curl -i "http://iot-agent:4041/iot/services/" \
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
curl -sS "http://iot-agent:4041/iot/services/" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"

ROBOTS=$(cat << __EOD__
[
  {
    "id": "jad01"
  },
  {
    "id": "jad02"
  }
]
__EOD__
)

# register devices
LEN=$(echo ${ROBOTS} | jq length)
count=0
if [ ${LEN} -gt 0 ]; then
  for i in $(seq 0 $((${LEN} - 1))); do
    robot_id=$(echo ${ROBOTS} | jq -r .[${i}].id)
    echo "${robot_id} will be registered."
    curl -i "http://iot-agent:4041/iot/devices/" \
         -H "Fiware-Service: ${FIWARE_SERVICE}" \
         -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
         -H "Content-Type: application/json" \
         -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "${robot_id}",
      "entity_name": "${robot_id}",
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
          "name": "robotSize",
          "type": "object"
        }
      ],
      "commands": [
        {
          "name": "naviCmd",
          "type": "command"
        },
        {
          "name": "stopCmd",
          "type": "command"
        }
      ],
      "transport": "HTTP",
      "endpoint": "http://localhost:3000/amqp10/cmd/${type}/${robot_id}"
    }
  ]
}
__EOS__
    let ++count
  done
fi
echo "${count} devices were registered."

# retrieve device
curl -sS "http://iot-agent:4041/iot/devices" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"

curl -sS "http://orion:1026/v2/entities?type=${type}" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}"
