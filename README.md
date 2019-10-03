![Flask](https://img.shields.io/pypi/pyversions/flask.svg)
# Sanus Solutions Server Project
## Getting Started
### Server Structure
There are several main components to the local server:  
1. Docker container for Flask webapp.  (via port 5000 on actual server machine ip)  
2. Docker container for Tensorflow Serving module for extracting face embeddings. (via port 8500 on assigned ip on docker network)  
3. Docker container for Tensorflow Serving module for MTCNN preprocessor. (via port 8501 on assigned ip on docker network)  
4. Docker network that connects all the containers.  
5. MongoDB running on server machine(Temporary).

### Prerequisites
#### 1. Install Docker
* [Install docker](https://docs.docker.com/install/), follow instruction for the OS where tensorflow serving model server will run (macos or linux).  
* The docker commands listed below might need be ran with root access: ```sudo```  

#### 2. Install Nvidia Driver and Nvidia Runtime for Docker 
* All containers with GPU support will only run on Linux host systems because the Nvidia Runtime ```nvidia-docker``` only supports Linux.  
* First install Nvidia driver for GPU: first check the list of packages for the gpu using: ```sudo ubuntu-drivers devices``` then use apt-get to install the driver package. For example:  
```sh
sudo ubuntu-drivers devices

== /sys/devices/pci0000:00/0000:00:03.1/0000:23:00.0 ==
vendor   : NVIDIA Corporation  
modalias : pci:v000010DEd00001B80sv00001462sd00003369bc03sc00i00  
driver   : nvidia-384 - distro non-free recommended  
driver   : xserver-xorg-video-nouveau - distro free builtin

sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-410
```  
Currently running nvidia-410(This is meant for the GTX1080 using right now). Refer to Nvidia dev forum for installation guide. 

* Then install the [NVIDIA Runtime](https://github.com/NVIDIA/nvidia-docker) ```nvidia-docker```:  
```sh
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge -y nvidia-docker

# Add the package repositories
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image. 
docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
```
#### 3. Install MongoDB
* Import the public key used by the package management system.
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```
* Create a list file for MongoDB(Ubuntu18.04).
```
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
```
* Install the MongoDB packages.
```
sudo apt-get install -y mongodb-org
```
Please refer to MongoDB Community for full installation guide([mongo ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition-using-deb-packages)). 

## Running and Testing
### Quick Start
1. Open a terminal and enter(skip ./build_server.sh if built before).
```sh
./build_server.sh
./run_server.sh
```
2. Open a second terminal and enter(skip ./build_tensorflow.sh if built before).
```sh
./build_tensorflow.sh
./run_tensorflow.sh
```
3. Open a third terminal and enter(skip ./build_mtcnn.sh if built before).
```sh
./build_mtcnn.sh
./run_mtcnn.sh
```
4. Open a forth terminal and enter.
```sh
./connect_services.sh
```
5. Open a fifth terminal and enter.
```sh
./run_mongodb.sh
```

### Manual Build/Run
#### Flask App Container with GPU Support for Dlib:  
* The Dockerfile Dockerfile.flask-app builds the container for the Flask app, port 5000 is exposed.  
* Building/Running the dockerfile(only needs to build ONCE): 
```sh
sudo docker build -t <app_image_name_here> -f Dockerfile.flask-app .
sudo docker run --name <app_container_name> -it -p 5000:5000 --rm <app_image_name_here>
``` 
Tags explained: ```-it```: interactive session, ```--rm```: container will be deleted once it exits, ```-p```: allow port traffic.  


### Tensorflow Serving (for Embeddings) with GPU support:  
* The TF serving container will only run on a Linux host machine because there's no runtime support for macOS and Windows.  
* The TF serving container with GPU support needs up-to-date NVIDIA driver and the NVIDIA Container Runtime ```nvidia-docker```.  
* The Dockerfile [Dockerfile.serving-gpu](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.serving-gpu) builds the TF serving container with gpu support.  
* Building/Running the Dockerfile(only needs to build ONCE): 
```sh
sudo docker build -t <serving_image_name_here> -f Dockerfile.serving-gpu .
sudo docker run --runtime=nvidia --name <serving_container_name> -it -p 8500:8500 --rm <serving_image_name_here>
``` 

### Mtcnn Serving with GPU Support:  
* The Dockerfile Dockerfile.mtcnn-serving-gpu builds the Mtcnn serving container with gpu support.  
* Building/Running the Dockerfile(only needs to build ONCE): 
```sh
sudo docker build -t <mtcnn_serving_image_name_here> -f Dockerfile.mtcnn-serving-gpu .
sudo docker run --runtime=nvidia --name <mtcnn_serving_container_name> -it -p 8501:8501 --rm <mtcnn_serving_image_name_here>
```  
### Connecting the Docker containers  
* First create a docker network using: 
```sh
sudo docker network create --driver=bridge --subnet=172.168.0.0/16 sanus-network
```
* The subnet ```172.168.0.0/16``` works with the default TF serving container ip address (```TF_HOST```) specified in config.py. The IP address of the Flask app container is not important since the communication with it from the camera nodes will be handled by the host machine, not the containers. Connect the flask app container with: 
```sh
sudo docker network connect sanus-network <app_container_name>
```  
* Then we need to connect the TF/Mtcnn serving containers to the network with an assigned ip address so the flask app can send request to the model server. Again, a default ip address is assigned in config.py. Connect the serving container to the network by: 
```sh
sudo docker network connect --ip 172.168.0.3 sanus-network <serving_container_name>
sudo docker network connect --ip 172.168.0.4 sanus-network <mtcnn_serving_container_name>
```  
### MongoDB Setup
* Edit /etc/mongod.conf to bind your ip to allow remote access.(only the FIRST TIME)
```sh
# network interfaces
net:
	port 27017
	bingIp: 127.0.0.1, [IP goes here]
```
* Start MongoDB. To verify if MongoDB is running, check /var/log/mongodb/mongod.log
```sh
sudo service mongod start
```
Refer to mongo folder README for more helpful resources.

## Known Issues and Notes
### Known issues
* Pretrained models trained on CASIA-WebFace and VGGFace2 has poor performance when it comes to Asian faces.
* Dlib preprocessor (face detector) will not work with large image.
### Docker
* Regularly check docker image and container usage. Remove any unused image/container if delete flag is not provided. 
```sh
sudo docker image ls
sudo docker image remove [image-id]
```
* Runtime log files are saved in container, to access container shell
```sh
sudo docker exec -it <app_container_name> bash
```
## Authors
* [Billy Zheng](https://github.com/hzheng40) - Docker, tensor-flow, mtcnn, flask
* [Klaus Zeng](https://github.com/klauszeng) - flask, MongoDB

## License
Copyright (c) <2019> <Sanus Solutions>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
