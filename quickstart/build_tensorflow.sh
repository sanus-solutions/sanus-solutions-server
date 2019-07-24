#!/bin/bash
cd /home/sanus/Desktop/sanus_face_server
sudo docker build -t tensorflow -f Dockerfile.serving-gpu . 