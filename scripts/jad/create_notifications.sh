#!/bin/bash

export FIWARE_SERVICE="demoservice"
export FIWARE_SERVICEPATH="/demo/path"
export id_pattern="robot"
export type="robot"

# delete subscriptions
EXISTING_SUBSCRIPTIONS=$(curl -sS -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-Servicepath: ${FIWARE_SERVICEPATH}" "http://localhost:1026/v2/subscriptions/?limit=1000")
LEN=$(echo ${EXISTING_SUBSCRIPTIONS} | jq length)
count=0
if [ ${LEN} -gt 0 ]; then
  for i in $(seq 0 $((${LEN} - 1))); do
    id=$(echo ${EXISTING_SUBSCRIPTIONS} | jq .[${i}].id -r)
    echo "${id} will be deleted."
    curl -i -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-Servicepath: ${FIWARE_SERVICEPATH}" "http://localhost:1026/v2/subscriptions/${id}" -X DELETE
    let ++count
  done
fi
echo "${count} entities were deleted."

# create pose subscription
curl -i -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" -H "Content-Type: application/json" "http://localhost:1026/v2/subscriptions/" -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "${id_pattern}.*",
      "type": "${type}"
    }],
    "condition": {
      "attrs": ["pose"]
    }
  },
  "notification": {
    "http": {
      "url": "http://host.docker.internal:3000/api/v1/notifications/pose"
    },
    "attrs": ["pose"]
  }
}
__EOS__

# create mode subscription
curl -i -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" -H "Content-Type: application/json" "http://localhost:1026/v2/subscriptions/" -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "${id_pattern}.*",
      "type": "${type}"
    }],
    "condition": {
      "attrs": ["mode"]
    }
  },
  "notification": {
    "http": {
      "url": "http://host.docker.internal:3000/api/v1/notifications/mode"
    },
    "attrs": ["mode"]
  }
}
__EOS__
