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
                        "latitude": 37.6307733,
                        "longitude": 141.0148266
                    },
                    "angle": {
                        "theta": 90
                    },
                    "speed": null,
                    "metadata": {
                        "map": "GPS"
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6307722,
                        "longitude": 141.0147974
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.630874,
                        "longitude": 141.0147982
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6308885,
                        "longitude": 141.01485
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6307728,
                        "longitude": 141.0148573
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6307733,
                        "longitude": 141.0148264
                    },
                    "angle": {
                        "theta": 90
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5,
                        "map": "Cartographer"
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": 37.6307714,
                        "longitude": 141.0146808
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
