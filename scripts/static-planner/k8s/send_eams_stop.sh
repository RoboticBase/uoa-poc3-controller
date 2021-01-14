#!/bin/bash

export FIWARE_SERVICE="uoapoc2020"
# export FIWARE_SERVICE="security"
export FIWARE_SERVICEPATH="/"
export type=robot
export id=robot01

# send command to device
curl -i "http://orion:1026/v2/entities/${id}/attrs?type=${type}" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
     -H "Content-Type: application/json" \
     -X PATCH -d @- <<__EOS__
{
    "naviCmd": {
        "type": "command",
        "value": {
            "time": "2020-09-22T05:06:07.890+00:00",
            "command": "stop",
            "waypoints": []
        }
    }
}
__EOS__
