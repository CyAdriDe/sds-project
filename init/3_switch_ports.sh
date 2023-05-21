#!/bin/bash

echo "Setting up bridge"
sudo ovs-vsctl set Bridge s4 protocols=OpenFlow13 && \
echo "Setting up port" && \
sudo ovs-vsctl add-port s4 s4-snort && \
sudo ovs-ofctl show s4
