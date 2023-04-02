# YOLOv7-inference-service

## Getting Started

### Pre-requirements
Install **nvidia-driver-520**(gpu, cuda-11.8), **nvidia-docker** and **docker** before installing the docker container.

- [Tutorial-nvidia-driver](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html)

- [Tutorial-docker](https://docs.docker.com/engine/install/ubuntu/)

- [Tutorial-nvidia-docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

###  Loading docker images or building image
**Loading docker images**
```shell
sudo chmod u+x ./docker/*.sh
sudo ./docker/download.sh
docker load < yolov7-server.tar
```
**building image**
```shell
sudo chmod u+x ./docker/*.sh
sudo ./docker/build.sh
```

###  Download yolov7
```shell
git clone https://github.com/WongKinYiu/yolov7.git
```

### Run docker container
```shell
sudo chmod u+x ./docker/*.sh
sudo ./docker/run.sh
```

### Run webAPI service

```python
python3 server.py -p 550
```
- p: The port number of server.

### Testing
```python
python3 client.py -p <folder/files>
```
- p: The path of inference images. you can input the folder path or the image path.

## Reference
- YOLOv7
    - https://github.com/WongKinYiu/yolov7