#!/bin/bash

# Update package lists
sudo apt-get update

# Install Python 3 and pip
sudo apt-get install -y python3 python3-pip

# Install required dependencies
sudo pip3 install -r requirements.txt