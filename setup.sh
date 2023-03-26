#!/bin/bash
HOME=$1

#setup CUDA & cuDNN
apt install gcc
apt-get install linux-headers-$(uname -r)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2004-12-1-local_12.1.0-530.30.02-1_amd64.deb
dpkg -i cuda-repo-ubuntu2004-12-1-local_12.1.0-530.30.02-1_amd64.deb
cp /var/cuda-repo-ubuntu2004-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/
apt-get update
apt-get -y install cuda
apt install nvidia-cuda-toolkit
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
apt-get update
apt-get install libcudnn8=8.8.0.121-1+cuda12.0
apt-get autoremove

#setup ssh for GitHub
#cd $HOME/.ssh
#ssh-keygen -t rsa
#cat id_rsa.pub 
#ssh -T git@github.com

#setup AugmentedNet
cd $HOME
#git clone --recursive git@github.com:Alicelavander/AugmentedNet.git
wget https://github.com/napulen/AugmentedNet/archive/refs/heads/main.zip
apt install unzip
unzip main.zip
mv AugmentedNet-main AugmentedNet
cd AugmentedNet/
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh
bash https://repo.anaconda.com/miniconda/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh
#apt install python3.8-venv
#python3 -m venv .env 
#source .env/bin/activate
#pip install -r requirements.txt
#wget https://github.com/napulen/AugmentedNet/releases/latest/download/dataset.zip
#unzip dataset.zip
#apt install unzip
#unzip dataset.zip

#nvidia-smi
