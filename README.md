# sds-project
## Running the topology
First install the dependencies with:
```
pip3 install -r requirements.txt
```
First, we had to start the Ryu Manager: 
```
sudo ryu-manager ~/ryu/ryu/app/simple_switch_13.py
```
After that you must run the topology with:
```
sudo mn -c && sudo python3 rotuerTopology.py
```

