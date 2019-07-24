#!/bin/bash
cd /home/sanus/Desktop/sanus_face_server
sudo docker build -t mtcnn -f Dockerfile.mtcnn-serving-gpu . 
