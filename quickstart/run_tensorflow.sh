#!/bin/bash
cd /home/sanus/Desktop/sanus_face_server
sudo docker run --runtime=nvidia --name tensorflow-container -it -p 8500:8500 --rm tensorflow 