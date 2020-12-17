#!/bin/bash

export FIWARE_SERVICE="demoservice"
export FIWARE_SERVICEPATH="/demo/path"
export type=plan

# function
iso8601() {
  echo $(date '+%Y-%m-%dT%H:%M:%S%z')
}

# delete entities
EXISTING_PLANS=$(curl -sS -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-Servicepath: ${FIWARE_SERVICEPATH}" "http://localhost:1026/v2/entities/?type=${type}&limit=1000&attrs=id")
LEN=$(echo ${EXISTING_PLANS} | jq length)
count=0
if [ ${LEN} -gt 0 ]; then
  for i in $(seq 0 $((${LEN} - 1))); do
    id=$(echo ${EXISTING_PLANS} | jq .[${i}].id -r)
    echo "${id} will be deleted."
    curl -i -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-Servicepath: ${FIWARE_SERVICEPATH}" "http://localhost:1026/v2/entities/${id}/?type=${type}" -X DELETE
    let ++count
  done
fi
echo "${count} entities were deleted."

# register entity
PLANS=$(cat << __EOD__
[
  {
    "plan_id": "plan01",
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
  },
  {
    "plan_id": "plan01r",
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
]
__EOD__
)

LEN=$(echo ${PLANS} | jq length)
count=0
if [ ${LEN} -gt 0 ]; then
  for i in $(seq 0 $((${LEN} - 1))); do
    plan_id=$(echo ${PLANS} | jq -r .[${i}].plan_id)
    waypoints=$(echo ${PLANS} | jq -r .[${i}].waypoints)
    echo "${plan_id} will be registerd."
curl -i "http://localhost:1026/v2/entities" \
     -H "Fiware-Service: ${FIWARE_SERVICE}" \
     -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" \
     -H "Content-Type: application/json" \
     -X POST -d @- <<__EOS__
{
  "id": "${plan_id}",
  "type": "${type}",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "$(iso8601)"
  },
  "waypoints": {
    "type": "array",
    "value": ${waypoints}
  }
}
__EOS__
    let ++count
  done
fi
echo "${count} entities were registered."

