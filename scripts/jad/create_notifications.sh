#!/bin/bash

export FIWARE_SERVICE="demoservice"
export FIWARE_SERVICEPATH="/demo/path"
export id_pattern="robot"
export type="robot"


# create subscription
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
