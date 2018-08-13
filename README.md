# Local Server structure  
There are two main components to the local server: the Flask webapp and the Tensorflow Serving module. Both of these components live in Docker containers, and the containers are connect via port 8500 on the TF serving container. And all communication between the camera nodes and the local server are through port 5000 on the Flask app container.

# Install Dependencies for local server 

# Install Docker
* Install docker, follow instruction for the OS where tensorflow serving model server will run (macos or linux).  
* The ```docker``` commands listed below might need be ran with root access: ```sudo docker```  

# Install Nvidia Drivers and Nvidia Runtime for docker
* This section is only for containers with GPU support. If you're only using the minimal containers without GPU support, you can skip this section.    
* All containers with GPU support will only run on Linux host systems because the Nvidia Runtime ```nvidia-docker``` only supports Linux.  
* Install Nvidia driver for GPU: first check the list of packages for the gpu using: ```sudo ubuntu-drivers devices``` then use apt-get to install the driver package. For example:  
```sh
sudo ubuntu-drivers devices

== /sys/devices/pci0000:00/0000:00:03.1/0000:23:00.0 ==
vendor   : NVIDIA Corporation  
modalias : pci:v000010DEd00001B80sv00001462sd00003369bc03sc00i00  
driver   : nvidia-384 - distro non-free recommended  
driver   : xserver-xorg-video-nouveau - distro free builtin

sudo apt-get install nvidia-384
```  

* Then install the NVIDIA Runtime ```nvidia-docker```:  
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

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
```

# Build the Dockerfiles and run containers  
## Flask app container without GPU support for Dlib:  
* The Dockerfile [Dockerfile.flask-app](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.flask-app) builds the container for the Flask app, port 5000 is exposed.  
* Building the dockerfile: ```docker build -t <app_image_name_here> -f Dockerfile.flask-app .``` (Installing dlib might take a bit.)  
* Running the docker container: ```docker run --name <app_container_name> -it -p 5000:5000 --rm <app_image_name_here>``` Tags explained: ```-it```: interactive session, ```--rm```: container will be deleted once it exits, ```-p```: allow port traffic.  
* Dlib will be slower when dealing with larger images since there's no gpu support.  

## Flask app container with GPU support for Dlib:
* The Dockerfile [Dockerfile.flask-app-gpu](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.flask-app-gpu) builds the container for the Flask app with Dlib compiled with CUDA and CuDnn, port 5000 is exposed.  
* Building the dockerfile: ```docker build -t <app_image_name_here> -f Dockerfile.flask-app-gpu .``` (Compiling dlib might take a bit.)  
* Running the docker container: ```docker run --runtime=nvidia --name <app_container_name> -it -p 5000:5000 --rm <app_image_name_here>``` Tags explained: ```--runtime=nvidia```: enable nvidia runtime in the docker container, ```-it```: interactive session, ```--rm```: container will be deleted once it exits, ```-p```: allow port traffic.  
* Still very unstable with larger images, especially when ran side by side with TF serving container with GPU support. Sometimes throws ```CUDNN_STATUS_BAD_PARAM``` error and sometimes cuda throws out of memory error. If these errors occur, reduce the image size and try again.  

## Tensorflow Serving without GPU support:  
* The Dockerfile [Dockerfile.serving-min](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.serving-min) builds the minimum container for tensorflow serving without gpu support.  
* Building the dockerfile: ```docker build -t <serving_image_name_here> -f Dockerfile.serving-min .```  
* Running the docker container: ``` docker run --name <serving_container_name> -it -p 8500:8500 --rm <serving_image_name_here>```

<!-- 1. There are 2 Dockerfiles. [Dockerfile](https://github.com/sanus-solutions/sanus-face-server/blob/master/Dockerfile) builds the minimal tensorflow serving container without GPU support, and [Dockerfile.devel](https://github.com/sanus-solutions/sanus-face-server/blob/master/Dockerfile.devel)(**Still in development**) builds the tensorflow serving container with GPU support. Note that the GPU support build uses bazel and will eat up all your RAM.  
2. Build the container with: ```docker build --pull -t <your_image_name_here> .```  
    or ```docker build --pull -t <your_image_name_here> -f Dockerfile.devel-gpu .``` 
3. Now run a container with: ```docker run --name <your_container_name_here> -it <your_image_name_here> bash```  
and this will start an interactive bash shell in the container. Now you can run the model server with the following:  
```tensorflow_model_server --port=8500 --model_name=saved_model --model_base_path=/models``` Now the model server should be running in your Docker container. Note that you might have to ```cd ..``` once you're in the container bash. Just make sure you're in a directory that there's a ```\models``` directory.   -->

## Tensorflow Serving with GPU support:  
* The TF serving container will only run on a Linux host machine because there's no runtime support for macOS and Windows.  
* The TF serving container with GPU support needs up-to-date NVIDIA driver and the NVIDIA Container Runtime ```nvidia-docker```.  
* The Dockerfile [Dockerfile.serving-gpu](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/Dockerfile.serving-gpu) builds the TF serving container with gpu support.  
* Building the Dockerfile: ```docker build -t <serving_image_name_here> -f Dockerfile.serving-gpu .```   
* Running the Docker container: ```docker run --runtime=nvidia --name <serving_container_name> -it -p 8500:8500 --rm <serving_image_name_here>```  

# Connecting the two Docker containers  
* First create a docker network using: ```docker network create --driver=bridge --subnet=<user_specified_subnet> <network_name>```, For example: ```docker network create --driver=bridge --subnet=172.168.0.0/16 sanus-network```. The subnet ```172.168.0.0/16``` works with the default TF serving container ip address (```TF_HOST```) specified in [config.py](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/config/config.py).
* The IP address of the Flask app container is not important since the communication with it from the camera nodes will be handled by the host machine, not the containers. Connect the flask app container with: ```docker network connect <network_name> <app_container_name>```.  
* Then we need to connect the TF serving container to the network with an assigned ip address so the flask app can send request to the model server. Again, a default ip address is assigned in [config.py](https://github.com/sanus-solutions/sanus_face_server/blob/server_dev/config/config.py). Connect the serving container to the network by: ```docker network connect --ip <assigned_ip_here> <network_name> <serving_container_name>```. For example: ```docker network connect --ip 172.168.0.3 sanus-network sanus_serving_container```
<!-- # Run the local server
In the virtual env that you installed all the dependencies:  
1. In the repo root: ```export FLASK_APP=app.py```
2. Run ```flask run --host=0.0.0.0```
3. You might have to do: ```iptables -I INPUT -p tcp --dport 5000 -j ACCEPT``` to allow port 5000 traffic for Flask.   -->

# Sending requests to the local server
* Check the local server's ip address in the router configuration page, and use that address in your request url in camera node clients.  