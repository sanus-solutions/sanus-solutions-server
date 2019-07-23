# Pymongo 

Temporary local database for storing embeddings

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

python2.7+ or 3.4+

### Installing

Please refer to MongoDB Community for full installation guide([mongo ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition-using-deb-packages)). 

1.Import the public key used by the package management system.

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```


2.Create a list file for MongoDB(Ubuntu18.04).

```
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
```

3.Install the MongoDB packages.

```
sudo apt-get install -y mongodb-org
```
## Run

### Start MongoDB 

Make sure App is connect to the right mongo ip 

```
sudo service mongod start
```

Remove lock for pymongo to access mongodb if being blocked 
```
sudo rm /var/lib/mongodb/mongod.lock
mongod --repair
sudo service mongod start
```

edit /etc/mongod.conf, bind your server ip to allow remote access

To verify if MongoDB is running, check /var/log/mongodb/mongod.log.

### Stop MongoDB

```
sudo service mongod stop
```

### Restart

```
sudo service mongod restart
```

### Shell

```
mongo
```
## Mongo Configuration
[DEFAULT]
Name = Mongo DB
LogLevel = DEBUG 

[MONGO]
URL = mongodb://{ip}:27017/ //binded port to access mongodb
Database = Hospital // name of the database
FaceCollection = FaceCollection // name of the embedding collection
UniqueID = true // no duplicated id/name is allowed if true

## Authors

Klaus

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