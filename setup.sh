#!/bin/bash  
cd ~/.ssh
#ssh-keygen -t rsa
#cat id_rsa.pub 
#ssh -T git@github.com
cd ~/
#git clone --recursive git@github.com:Alicelavander/AugmentedNet.git
wget https://github.com/napulen/AugmentedNet/archive/refs/heads/main.zip
apt install unzip
unzip main.zip
mv AugmentedNet-main AugmentedNet
#python --version
#python3 --version
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-12-1_12.1.0-1_amd64.deb
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
#wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
#sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo dpkg -i cuda-12-1_12.1.0-1_amd64.deb
sudo apt-get update
sudo apt-get install cuda-12-1
cd AugmentedNet/
#python3 -m venv .env 
#sudo apt install python3.8-venv
#python3 -m venv .env 
#source .env/bin/activate
#pip install -r requirements.txt
#wget https://github.com/napulen/AugmentedNet/releases/latest/download/dataset.zip
#unzip dataset.zip
#sudo apt install unzip
#unzip dataset.zip
