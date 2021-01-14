#!/bin/bash

export FIWARE_SERVICE="uoapoc2020"
export FIWARE_SERVICEPATH="/"
export id_pattern="robot"
export type="robot"

# create pose subscription
curl -i -H "Fiware-Service: ${FIWARE_SERVICE}" -H "Fiware-ServicePath: ${FIWARE_SERVICEPATH}" -H "Content-Type: application/json" "http://orion:1026/v2/subscriptions/" -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "${id_pattern}.*",
      "type": "${type}"
    }],
    "condition": {
      "attrs": ["mode", "pose", "time"]
    }
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    },
    "attrs": ["mode", "pose", "time"]
  }
}
__EOS__
