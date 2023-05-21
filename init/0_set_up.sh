#!/bin/bash
echo "Installing dependencies"
sudo pip3 install -r ../requirements.txt

echo "\n ***Installing packages"
sudo apt-get install -y snort && sudo apt-get install -y nmap

echo "\n ***Copying snort files to snort local config"

sudo cp ../snort/*conf /etc/snort/ && \
sudo chown snort:snort /etc/snort/*.conf && \
sudo cp ../snort/*rules /etc/snort/rules/ && \
sudo systemctl restart snort

echo "\n ***Setting snort inteface"

sudo ip link add name s4-snort type dummy && \
sudo ip link set s4-snort up
