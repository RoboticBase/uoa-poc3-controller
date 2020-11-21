#!/bin/bash
cmd="/var/lib/artemis/bin/artemis"
user=artemis
password=simetraehcapa
type=robot

ids=("robot01" "robot02")
suffixes=("up" "down")
for id in "${ids[@]}"; do
  for suf in "${suffixes[@]}"; do
    docker exec -t dynamic-planner_activemq_1 \
      ${cmd} queue create --user ${user} --password ${password} \
      --name ${type}.${id}.${suf} --address ${type}.${id}.${suf} \
      --anycast --no-durable --preserve-on-no-consumers --auto-create-address
  done 
done

