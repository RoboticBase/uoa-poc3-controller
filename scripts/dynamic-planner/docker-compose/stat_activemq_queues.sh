#!/bin/bash
cmd="/var/lib/artemis/bin/artemis"
user=artemis
password=simetraehcapa
type=robot

docker exec -t dynamic-planner_activemq_1 \
  ${cmd} queue stat --user ${user} --password ${password} \
  --queueName ${type}
