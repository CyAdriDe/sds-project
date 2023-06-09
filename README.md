# SDS-Project-MCYBERS23'
## 1. Topology
<img src="./resources/img/topo.png"
     alt="Topology of the project"
     style="float: left; margin-right: 10px;" />
## 2. Running ONLY the Mininet topology to first tests
First install the dependencies with:
```
pip3 install -r requirements.txt
```
First, we have to start the Ryu Manager (with a simple_switch_13.py to test):
```
sudo ryu-manager ~/ryu/ryu/app/simple_switch_13.py
```
After that you must run the topology with:
```
sudo mn -c && sudo python3 routerTopology.py
```
## 3. Mininet Topology + Snort (production scripts)
### 3.1. Snort preparation
```
sudo apt-get install snort
```
To add snort rules, open the file located in /etc/snort/rules named Myrules.rules. Inside this file, put the following line:
```
include $RULE_PATH/Myrules.rules
```
And comment this other one (one example could be the ICMP if another rule is set). Remember to comment all the lines that are related with the rules that you want to implement, to avoid the duplicate elements:
```
#$RULE_PATH/icmp-info.rules 
```
For setup the Snort, run the following commands (creating a new s4-snort interface). Run these commands:
```
sudo ip link del s4-snort & sudo ip link add name s4-snort type dummy && sudo ip link set s4-snort up && sudo ovs-vsctl add-port s4 s4-snort && sudo ovs-ofctl show s4
```
The simple_switch_snort.py is located in ~/ryu/ryu/app/. NOTE: change the line 72 by this one:
```
print('alertmsg: %s' % msg.alertmsg[0].decode())
```
### 3.2. Running Mininet + Snort
Then, to verify the snort behaviour, run in different terminals:
```
sudo python3 routerProject.py
```
```
sudo ryu-manager ~/ryu/ryu/app/simple_switch_snort.py
```
```
sudo ip link del s4-snort && sudo ip link add name s4-snort type dummy && sudo ip link set s4-snort up && sudo ovs-vsctl add-port s4 s4-snort && sudo ovs-ofctl show s4
```
```
sudo snort -i s4-snort -A unsock -l /tmp -c /etc/snort/snort.conf
```
The previous commands allow to run the Mininet + Snort + LoadBalancer.
This command HAS to be performed to stop executing Mininet and Snort:
```
sudo kill -9 $(ps aux | grep 'snort' | awk '{print $2}') && sudo systemctl restart snort.service
```
When you stop the Mininet, always RUN to clear the cache:
```
sudo mn -c
```
NOTE: the following commands are the routes to the SNORT files (ignore them):
```
sudo cp ../snort/conf /etc/snort/ && \
sudo chown snort:snort /etc/snort/.conf && \
sudo cp ../snort/*rules /etc/snort/rules/
```
## Load Balancer: how does it work?
For implementing the load balancer we implemented an haproxy to work as a balancer.
```
sudo apt-get install haproxy && sudo systemctl stop haproxy
```
You will notice that we stop the haproxy service since we will launch it at the start of the mininet with a custom configuration.

If you look at the **resources/haproxy.cfg** file you can see the configuration, but the important part is the balancing algorithm. We choose the roundrobin algorithm, which works by equally distributing the load in a circular way between the pool of servers, in our case the 2 servers in the DMZ. In this case is equally distributed because we weighted both servers equally but we can distribute the load balancing if we have a server that can handle more petitions per second we can change it.

Also, haproxy checks the connection to the servers, so if one is down it distributes all the load to the one available.

## 4. Grafana part: procedure and commands
Installing InfluxDB with:
```
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.8.4_amd64.deb &&
sudo dpkg -i influxdb_1.8.4_amd64.deb &&
sudo apt-get update &&
sudo apt-get install -yq python3-influxdb &&
rm influxdb_1.8.4_amd64.deb
```
Starting and testing InfluxDB:
```
sudo systemctl start influxdb &&
influx
```
Now, install the Telegraf with:
```
wget https://dl.influxdata.com/telegraf/releases/telegraf_1.17.3-1_amd64.deb &&
sudo dpkg -i telegraf_1.17.3-1_amd64.deb && 
rm telegraf_1.17.3-1_amd64.deb &&
sudo mv /etc/telegraf/telegraf.conf /etc/telegraf/telegraf.conf.bup && sudo cp ../telegraf/telegraf.conf /etc/telegraf/
```
Now, install Grafana with:
```
sudo apt-get install -y libfontconfig1 &&
wget https://dl.grafana.com/oss/release/grafana_7.4.3_amd64.deb &&
sudo dpkg -i grafana_7.4.3_amd64.deb &&
rm grafana_7.4.3_amd64.deb
```
```
sudo systemctl start grafana-server &&
sudo systemctl restart grafana-server
```
## 5. Firewall rules
```
sudo ryu-manager ryu/ryu/app/rest_firewall.py ryu/ryu/app/simple_switch_snort.py ryu/ryu/app/simple_monitor_13_telegraf.py 
```
```
curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000001 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000002 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000003 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000004 && curl http://localhost:8080/firewall/module/status
```


