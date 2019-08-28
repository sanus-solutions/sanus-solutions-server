#!/bin/bash
sudo docker run --runtime=nvidia --name mtcnn-container -it -p 8501:8501 --rm mtcnn 
