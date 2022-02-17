#!/bin/bash

sudo apt update  
sudo apt -y upgrade  
python3 -m pip install --upgrade pip  
python3 -m pip install opencv-python==4.5.1.48
sudo apt install libatlas-base-dev libjasper-dev -y
sudo apt install ffmpeg  libcanberra-gtk3-module v4l-utils qv4l2 -y
sudo apt install -y postfix git awscli
pip3 install awscli boto3 pysimplegui numpy --upgrade

cd /usr/bin
sudo rm python
sudo ln -s python3 python
cd

sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show
sudo ./MPI4008-show

