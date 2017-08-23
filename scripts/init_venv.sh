#!/usr/bin/env bash
# -*- encoding UTF-8 -*-
# Author: Johny

# 在 Linux 上:

#sudo apt-get install python-pip python-dev python-virtualenv

# 在 Mac 上:

# 如果还没有安装 pip
#sudo easy_install pip

# 如果没有安装 virtualenv
# sudo pip install --upgrade virtualenv

mkdir -pv ~/tensorflow

cd ~/tensorflow

virtualenv --system-site-packages ~/tensorflow/venv/

cd ~/tensorflow/venv/

source bin/activate

# 安装 tensorflow

#pip install tensorflow

pip install https://storage.googleapis.com/tensorflow/mac/tensorflow-0.5.0-py2-none-any.whl

# pip install --upgrade <$url_to_binary.whl>

echo "Init tensorflow python env success"

