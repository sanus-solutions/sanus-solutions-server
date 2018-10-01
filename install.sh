#!/bin/bash
# install script for local servers
# author: Hongrui Zheng
echo Checking installed packages...

# Docker
echo Checking Docker...
DOCKER_OK=$(dpkg-query -W --showformat='${Status}\n' docker-ce | grep "install ok installed")
if ["" == "$DOKCER_OK"]; then
    echo "docker-ce not installed. Setting up now."
    echo "Removing earlier version of Docker..."
    sudo apt-get -y -qq remove docker docker-engine docker.io
    echo "Setting up Docker repository..."
    sudo apt-get -y -qq update
    sudo apt-get -y -qq install \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository -qq -y \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    sudo apt-get -y -qq update
    sudo apt-get -y -qq install docker-ce
    echo "Docker Installed"
fi

# Nvidia
# not sure if this will work
# driver
echo Getting Recommended gpu driver information...
RECO_DRVIER_VER=$(sudo ubuntu-drivers devices | grep recommended | awk '{ print$3 }')
echo The recommended driver is $RECO_DRVIER_VER
echo Installing $RECO_DRVIER_VER
sudo apt-get -y -qq install $RECO_DRVIER_VER
echo Nvidia Driver installed
# docker runtime
echo Installing docker nvidia runtime
echo Removing older version of nvidia-docker
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get -y -qq purge nvidia-docker
echo Adding nvidia-docker2 repository
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
    sudo apt-key -y -qq add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get -y -qq update
echo Installing nvidia-docker2
sudo apt-get -y -qq install nvidia-docker2
echo Reloading Docker daemon config
sudo pkill -SIGHUP dockerd
echo Testing nvidia-docker runtime
sudo docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
if [ $? -eq 0]; then
    echo Nvidia Docker runtime installed successfully
    echo Installation done
    exit 0
else
    echo Nvidia Docker runtime install failed
    exit 1
fi
