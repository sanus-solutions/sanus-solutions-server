#!/bin/bash
sudo docker run -it --name=flask-container --mount type=bind,source=/home/sanus-jhm/sanus_solutions_server,destination=/sanus_solutions_server -p 5000:5000 flask
