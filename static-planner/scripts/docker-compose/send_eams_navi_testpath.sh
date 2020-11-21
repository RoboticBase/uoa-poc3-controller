#!/bin/bash

export FIWARE_SERVICE="demoservice"
export FIWARE_SERVICEPATH="/demo/path"
export type=robot
export id=robot01

# send command to device
curl -i "http://localhost:1026/v2/entities/${id}/attrs?type=${type}" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
     -H "Content-Type: application/json" \
     -X PATCH -d @- <<__EOS__
{
    "naviCmd": {
        "type": "command",
        "value": {
            "time": "2020-09-22T05:06:07.890+00:00",
            "command": "start",
            "waypoints": [
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.63077812,
                        "longitude": 141.01482954
                    },
                    "angle": {
                        "theta": 270
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 120,
                        "map": 1
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6306639,
                        "longitude": 141.0148239
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 2
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.63077812,
                        "longitude": 141.01482954
                    },
                    "angle": {
                        "theta": 270
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 90,
                        "map": 2
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6307300,
                        "longitude": 141.0149716
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null
                }
            ]
        }
    }
}
__EOS__
