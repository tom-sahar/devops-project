#!/bin/bash

# Scale up to 5 replicas
scale_up() {
  echo "Scaling up the app to 5 replicas..."
  docker-compose up -d --scale app=5 --build
}

# Scale down to 3 replicas 
scale_down() {
  echo "Scaling down the app to 3 replicas..."
  docker-compose up -d --scale app=3 --build
}

if [ "$1" == "up" ]; then
  scale_up
elif [ "$1" == "down" ]; then
  scale_down
else
  echo "Usage: $0 {up|down}"
fi
