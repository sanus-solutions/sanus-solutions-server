#!/bin/bash
cd /home/sanus/Desktop/sanus_solutions_server/
sudo docker build -t tensorflow -f Dockerfile.serving-gpu . 
