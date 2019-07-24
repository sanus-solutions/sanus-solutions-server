#!/bin/bash
# run script for local server
# author: Hongrui Zheng

# Build images
echo Building app Dockerfile...
sudo docker build -t flask-app -f Dockerfile.flask-app .
echo Building MTCNN Dockerfile...
sudo docker build -t mtcnn-gpu -f Dockerfile.mtcnn-serving-gpu .
echo Building Embeddings Dockerfile...
sudo docker build -t emb-gpu -f Dockerfile.serving-gpu .

