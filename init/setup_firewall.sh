#!/bin/bash
sudo ovs-vsctl set bridge s1 protocols=OpenFlow13 && sudo ovs-vsctl set bridge s2 protocols=OpenFlow13 && sudo ovs-vsctl set bridge s3 protocols=OpenFlow13 && sudo ovs-vsctl set bridge s4 protocols=OpenFlow13

curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000001 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000002 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000003 && curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000004 && curl http://localhost:8080/firewall/module/status

#Allow internal pings (between subnet 1 <-> subnet 2)
curl -X POST -d  '{"nw_src": "192.168.0.0/24", "nw_dst": "192.168.1.0/24", "nw_proto":"ICMP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "192.168.1.0/24", "nw_dst": "192.168.0.0/24", "nw_proto":"ICMP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "192.168.0.0/24", "nw_dst": "192.168.1.0/24", "nw_proto":"ICMP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "192.168.1.0/24", "nw_dst": "192.168.0.0/24", "nw_proto":"ICMP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

#Allow to all users to access to HTTP server
	#For switch 1
curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001
	#For switch 2
curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000002
	#For switch 3
curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000003
	#For switch 4
curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.1/12", "nw_dst": "172.16.0.0/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"TCP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

curl -X POST -d  '{"nw_src": "172.16.0.0/12", "nw_dst": "172.16.0.1/12", "nw_proto":"UDP", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000004

# Deny SSH connections
curl -X POST -d  '{"nw_dst": "172.16.0.0/12", "tp_dst": "22", "nw_proto":"TCP", "actions": "DENY","priority": "11"}' http://localhost:8080/firewall/rules/0000000000000003

# Only SSH connection allowed for the s2u1 host
curl -X POST -d  '{"nw_src": "192.168.1.101/24", "nw_dst": "172.16.0.0/12", "tp_dst": "22", "nw_proto":"TCP", "priority": "12"}' http://localhost:8080/firewall/rules/0000000000000003


