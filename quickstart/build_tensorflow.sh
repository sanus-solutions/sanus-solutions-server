#!/bin/bash
cd /home/sanus-jhm/sanus_solutions_server
sudo docker build -t tensorflow -f Dockerfile.serving-gpu . 
