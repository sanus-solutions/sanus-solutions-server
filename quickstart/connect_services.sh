#!/bin/bash
sudo docker network connect sanus-jhm-network flask-container &&
sudo docker network connect --ip 172.168.0.3 sanus-jhm-network tensorflow-container &&
sudo docker network connect --ip 172.168.0.4 sanus-jhm-network mtcnn-container 
