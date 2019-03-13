#!/bin/bash
echo "Update apt cache"
apt update
echo "Install python-pip"
apt -y install python-pip
echo "Update pyOpenSSL pip package"
pip install --upgrade pyOpenSSL
echo "Install ansible"
pip install ansible
