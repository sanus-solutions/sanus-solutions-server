# I. KNOWN ISSUES:
* Pretrained models trained on CASIA-WebFace and VGGFace2 has poor performance when it comes to Asian faces.
* Dlib preprocessor (face detector) will not work with large image.
* Gunicorn experienced error [critical] worker timeout(pid:49). 
* Face_embedding storage is on local. Every Gunicorn worker has its own copy.

# II. Local Server structure  
There are several main components to the local server:  
* Docker container for Flask webapp.  (via port 5000 on actual server machine ip)  
* Docker container for Tensorflow Serving module for MTCNN preprocessor. (via port 8500 on assigned ip on docker network)  
* Docker container for Tensorflow Serving module for extracting face embeddings. (via port 8500 on assigned ip on docker network)  
* Docker network that connects all the containers.  

# III. Install Dependencies for local server:  

## 1. Install Docker
* Install docker, follow instruction for the OS where tensorflow serving model server will run (macos or linux).  
* The ```docker``` commands listed below might need be ran with root access: ```sudo docker```  

## 2. Install Nvidia Driver and Nvidia Runtime for docker
* This section is only for containers with GPU support. If you're only using the minimal containers without GPU support, you can skip this section.    
* All containers with GPU support will only run on Linux host systems because the Nvidia Runtime ```nvidia-docker``` only supports Linux.  
* First install Nvidia driver for GPU: first check the list of packages for the gpu using: ```sudo ubuntu-drivers devices``` then use apt-get to install the driver package. For example:  
```sh
sudo ubuntu-drivers devices

== /sys/devices/pci0000:00/0000:00:03.1/0000:23:00.0 ==
vendor   : NVIDIA Corporation  
modalias : pci:v000010DEd00001B80sv00001462sd00003369bc03sc00i00  
driver   : nvidia-384 - distro non-free recommended  
driver   : xserver-xorg-video-nouveau - distro free builtin

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

## 3. Build the Dockerfiles and run containers  
There are three containers you need to run (two if using Dlib preprocessor, which is not recommeded because of memory issues with larger images.)  
### - Flask app container without GPU support for Dlib:  
* This should be used as the default because the default preprocessor using MTCNN will be running in a seperate docker container.  
* The Dockerfile [Dockerfile.flask-app](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.flask-app) builds the container for the Flask app, port 5000 is exposed.  
* Building the dockerfile(Installing dlib might take a bit.)  : 
```sh
docker build -t <app_image_name_here> -f Dockerfile.flask-app .
```
* Running the docker container: 
```sh
docker run --name <app_container_name> -it -p 5000:5000 --rm <app_image_name_here>
``` 
Tags explained: ```-it```: interactive session, ```--rm```: container will be deleted once it exits, ```-p```: allow port traffic.  
* Dlib will be slower when dealing with larger images since there's no gpu support.  

### - Tensorflow Serving (for Embeddings) with GPU support:  
* The TF serving container will only run on a Linux host machine because there's no runtime support for macOS and Windows.  
* The TF serving container with GPU support needs up-to-date NVIDIA driver and the NVIDIA Container Runtime ```nvidia-docker```.  
* The Dockerfile [Dockerfile.serving-gpu](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.serving-gpu) builds the TF serving container with gpu support.  
* Building the Dockerfile: 
```sh
docker build -t <serving_image_name_here> -f Dockerfile.serving-gpu .
```   
* Running the Docker container: 
```sh
docker run --runtime=nvidia --name <serving_container_name> -it -p 8500:8500 --rm <serving_image_name_here>
``` 

### - Mtcnn Serving with GPU support:  
* The Dockerfile Dockerfile.mtcnn-serving-gpu builds the Mtcnn serving container with gpu support.  
* Building the Dockerfile: 
```sh
docker build -t <mtcnn_serving_image_name_here> -f Dockerfile.mtcnn-serving-gpu .
```   
* Running the Docker container: 
```sh
docker run --runtime=nvidia --name <mtcnn_serving_container_name> -it -p 8501:8501 --rm <mtcnn_serving_image_name_here>
```  

## 4. Connecting the Docker containers  
###First create a docker network using: 
```sh
docker network create --driver=bridge --subnet=<user_specified_subnet> <network_name>
```
For example: 
```sh
docker network create --driver=bridge --subnet=172.168.0.0/16 sanus-network
```
The subnet ```172.168.0.0/16``` works with the default TF serving container ip address (```TF_HOST```) specified in [config.py](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/config/config.py).
The IP address of the Flask app container is not important since the communication with it from the camera nodes will be handled by the host machine, not the containers. Connect the flask app container with: 
```sh
docker network connect sanus-network flask
```  
Then we need to connect the TF/Mtcnn serving containers to the network with an assigned ip address so the flask app can send request to the model server. Again, a default ip address is assigned in [config.py](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/config/config.py). Connect the serving container to the network by: 
```sh
docker network connect --ip <assigned_ip_here> <network_name> <serving_container_name>
```
For example: 
```sh
docker network connect --ip 172.168.0.3 sanus-network tf_serving_container
docker network connect --ip 172.168.0.4 sanus-network mtcnn_serving_container
```  