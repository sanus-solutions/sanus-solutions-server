#!/bin/bash

echo Building rekognition Dockerfile...
docker build -t rekognition . 
echo Running app
docker run --name rekognition_container -it -p 8000:8000 --rm rekognition
