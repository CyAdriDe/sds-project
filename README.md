# sds-project

## Topology
<img src="./resources/img/topo.png"
     alt="Topology of the project"
     style="float: left; margin-right: 10px;" />
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
## Once the Mininet is running, start Snort
```
sudo apt-get install snort
```
To add snort rules, open the file located in /etc/snort/rules named Myrules.rules. Inside this file, put the following line:
```
include $RULE_PATH/Myrules.rules
```
And comment this other one (one example could be the ICMP if another rule is set):
```
$RULE_PATH/icmp-info.rules 
```
For setup the Snort, run the following commands (r0 could be renamed). Check before run the commands:
```
sudo ip link add name r0-snort type dummy &&
sudo ip link set r0-snort up
```
The simple_switch_snort.py is located in ~/ryu/ryu/app/. NOTE: change the line 72 by this one:
```
print('alertmsg: %s' % msg.alertmsg[0].decode())
```
Then, to verify the snort behaviour, run in different terminals first the python3 and then the ovs-vsctl:
```
sudo python3 routerProject.py
```
```
sudo ovs-vsctl add-port r0 r0-snort &&
sudo ovs-ofctl show r0
```
```
sudo ryu-manager ~/ryu/ryu/app/simple_switch_snort.py
```

## Once the Mininet and Snort are running, it's time to start the Load Balancer in the s3 - DMZ switch, with 2 HTTP servers inside the subnet

