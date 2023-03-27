#!/bin/bash

#setup ssh for GitHub
#cd $HOME/.ssh
#ssh-keygen -t rsa
#cat id_rsa.pub
#ssh -T git@github.com

#setup AugmentedNet
#git clone --recursive git@github.com:Alicelavander/AugmentedNet.git
wget https://github.com/napulen/AugmentedNet/archive/refs/heads/main.zip
apt install unzip
unzip main.zip
mv AugmentedNet-main AugmentedNet
cd AugmentedNet/
wget https://github.com/napulen/AugmentedNet/releases/latest/download/dataset.zip
unzip dataset.zip
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh
bash Miniconda3-py38_23.1.0-1-Linux-x86_64.sh

#pip install -r requirements.txt
