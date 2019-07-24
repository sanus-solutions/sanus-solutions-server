#!/bin/bash
cd /home/sanus/Desktop/sanus_face_server
sudo docker run --name flask-container -it -p 5000:5000 --rm flask 