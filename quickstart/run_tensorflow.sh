#!/bin/bash
sudo docker run --runtime=nvidia --name tensorflow-container -it -p 8500:8500 --rm tensorflow 