#!/bin/bash

echo "Running SNORT"
sudo snort -i s4-snort -A unsock -l /tmp -c /etc/snort/snort.conf
