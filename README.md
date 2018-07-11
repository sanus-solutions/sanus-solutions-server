# Install Dependencies 
## Recommeded: use virtulaenv 
In a virtual env:  
1. ```pip install --upgrade tensorflow ```  
2. ```pip install tensor-serving-api```  
3. Download dlib source code from dlib.net, untar, enter directory and ```python setup.py install```  
4. ```pip install -r requirements.txt``` 

# Install Docker
1. Install docker, follow instruction for the OS where tensorflow serving model server will run (macos or linux).  
2. After docker is install and you have the docker image as a .tar on your system, run: ```docker run -it -p 8500:8500 <docker_image_name>.tar -name <give_your_container_whatever_name_you_want>```  
3. In the docker container bash, run: ```tensorflow_model_server --port=8500 --model_name=saved_model --model_base_path=/model/``` 