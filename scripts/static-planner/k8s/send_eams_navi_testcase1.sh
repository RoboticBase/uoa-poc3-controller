#!/bin/bash

# export FIWARE_SERVICE="uoapoc2020"
export FIWARE_SERVICE="security"
export FIWARE_SERVICEPATH="/"
export type=robot
export id=robot01

p1=(37.6307075583 141.014775192)
p2=(37.6307685533 141.014775632)
p3=(37.6307695 141.0146828)
p4=(37.6307675583 141.014807592)
p5=(37.630870115 141.014811423)
p6=(37.6312103967 141.014817323)
p7=(37.63121135 141.014781435)
p8=(37.6312078833 141.014851263)
p9=(37.6311116467 141.014848578)
p10=(37.630765695 141.01484295)

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
            "command": "start",
            "waypoints": [
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p3[0]},
                        "longitude": ${p3[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": 90
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5,
                        "map": "GPS"
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p4[0]},
                        "longitude": ${p4[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p5[0]},
                        "longitude": ${p5[1]}
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
                        "latitude": ${p6[0]},
                        "longitude": ${p6[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p7[0]},
                        "longitude": ${p7[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 10
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p6[0]},
                        "longitude": ${p6[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p8[0]},
                        "longitude": ${p8[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p9[0]},
                        "longitude": ${p9[1]}
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
                        "latitude": ${p10[0]},
                        "longitude": ${p10[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p4[0]},
                        "longitude": ${p4[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": 270
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
                        "latitude": ${p3[0]},
                        "longitude": ${p3[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                        "delay": 5
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p2[0]},
                        "longitude": ${p2[1]}
                    },
                    "angle": {
                        "theta": null
                    },
                    "speed": null,
                    "metadata": {
                    }
                },
                {
                    "point": {
                        "altitude": 0,
                        "latitude": ${p1[0]},
                        "longitude": ${p1[1]}
                    },
                    "angle": {
                        "theta": 0
                    },
                    "speed": null,
                    "metadata": {
                    }
                }
            ]
        }
    }
}
__EOS__
