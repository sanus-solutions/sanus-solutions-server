#!/bin/bash
cd /home/sanus-jhm/sanus_solutions_server
sudo docker build -t mtcnn -f Dockerfile.mtcnn-serving-gpu . 
