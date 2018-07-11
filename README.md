# Install Dependencies 
## Recommeded: use virtualenv 
In a virtual env:  
1. ```pip install --upgrade tensorflow ```  
2. ```pip install tensor-serving-api```  
3. Download dlib source code from dlib.net, untar, enter directory and ```python setup.py install```  
4. ```pip install -r requirements.txt``` 

# Install Docker
1. Install docker, follow instruction for the OS where tensorflow serving model server will run (macos or linux).  
2. There are 2 Dockerfiles. [Dockerfile](https://github.com/sanus-solutions/sanus-face-server/blob/master/Dockerfile) builds the minimal tensorflow serving container without GPU support, and [Dockerfile.devel](https://github.com/sanus-solutions/sanus-face-server/blob/master/Dockerfile.devel) builds the tensorflow serving container with GPU support. Note that the GPU support build uses bazel and will eat up all your RAM.  
3. Build the container with: ```docker build --pull -t <your_container_name_here> .``` or ```docker build --pull -t <your_container_name_here> -f Dockerfile.devel-gpu .``` 