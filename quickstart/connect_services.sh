#!/bin/bash
sudo docker network connect sanus-network flask-container &&
sudo docker network connect --ip 172.168.0.3 sanus-network tensorflow-container &&
sudo docker network connect --ip 172.168.0.4 sanus-network mtcnn-container 