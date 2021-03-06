#!/bin/bash
echo "Update apt cache"
apt update
echo "Install python-pip and setup tools"
apt -y install python-pip python-setuptools python-wheel
echo "Update pyOpenSSL pip package"
pip install --upgrade pyOpenSSL
echo "Install ansible"
pip install ansible
