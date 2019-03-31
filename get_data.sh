#!/bin/bash

cd "[Star-Wars-Chat-Bot]data/Scripts"
wget https://github.com/KunyuHe/Star-Wars-Chat-Bot/raw/master/%5BStar-Wars-Chat-Bot%5Ddata/Scripts.tar
tar -xvf Scripts.tar
rm Scripts.tar
cd ..
cd ..

cd "[Star-Wars-Chat-Bot]train/pre-trained weights"
wget https://www.dropbox.com/s/ss8nnkfzgwazfyy/JediChatPreTrained.h5?dl=1
cd ..
cd ..

wget https://github.com/KunyuHe/Star-Wars-Chat-Bot/raw/master/%5BStar-Wars-Chat-Bot%5Ddata/JediMaster.jpg
