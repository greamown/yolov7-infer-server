#!/bin/bash
# ---------------------------------------------------------

# Color ANIS
RED='\033[1;31m';
BLUE='\033[1;34m';
GREEN='\033[1;32m';
YELLOW='\033[1;33m';
CYAN='\033[1;36m';
NC='\033[0m';
# ---------------------------------------------------------

echo -e "${YELLOW}"
echo "$(date +"%T") Initialize ... "
echo -e "${NC}"

apt-get update -qy
apt install -qy software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt install -qy python3.9
apt install -qy curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
apt install -qy python3.9-distutils
python3.9 get-pip.py
echo 'export PATH=~/.local/bin/:$PATH' >> ~/.bashrc
source ~/.bashrc

echo -e "${RED}"
echo "$(date +"%T") Setting python3.9 ... "
echo -e "${NC}"

alias python3=python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python3
rm -r /usr/bin/python3.8

# ---------------------------------------------------------

echo -e "${YELLOW}"
echo "$(date +"%T") Install opencv-package ... "
echo -e "${NC}"
apt update -qy 
apt install -qy ffmpeg libsm6 libxext6
apt install -qy libxrender-dev
# ---------------------------------------------------------

echo -e "${YELLOW}"
echo "$(date +"%T") Install requirements.txt ... " 
echo -e "${NC}"
pip install -r docker/requirements.txt