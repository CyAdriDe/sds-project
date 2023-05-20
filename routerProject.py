#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
import time

class LinuxRouter( Node ):
    
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
    	# Disable forwarding when terminating
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    def build( self, **_opts ):
	
	# Define networks and router
        subnet1 = '192.168.0.1/24'
        subnet2 = '192.168.1.1/24'
        dmz = '172.16.0.1/12'
        ext = '147.0.0.1/12'
        router = self.addNode( 'r0', cls=LinuxRouter, ip=subnet1 , mac='00:00:00:00:00:00')
        
    # Add switches
        s1, sDMZ, s2, sEXT = [ self.addSwitch( s ) for s in ( 's1', 's3', 's2', 's4' ) ]
	
	# Add router links
        self.addLink(s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : subnet1 } )
        self.addLink(sDMZ, router, intfName2='r0-eth3',
                      params2={ 'ip' : dmz } )
        self.addLink(s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : subnet2 } )
        self.addLink(sEXT, router, intfName2='r0-eth4',
                      params2={ 'ip' : ext} )

    # Add hosts
        s1u1 = self.addHost( 's1u1', ip='192.168.0.101/24', mac='00:00:00:00:01:01',
                           defaultRoute='via 192.168.0.1' )
        s1u2 = self.addHost( 's1u2', ip='192.168.0.102/24', mac='00:00:00:00:01:02',
                           defaultRoute='via 192.168.0.1' )
        s2u1 = self.addHost( 's2u1', ip='192.168.1.101/8', mac='00:00:00:00:02:01',
                           defaultRoute='via 192.168.1.1' )
        s2u2 = self.addHost( 's2u2', ip='192.168.1.102/8', mac='00:00:00:00:02:02',
                           defaultRoute='via 192.168.1.1' )
                          
    # Add DMZ hosts
        dmzserver1 = self.addHost( 'dmzserver1', ip='172.16.0.101/12', mac='00:00:00:00:DD:01',
                           defaultRoute='via 172.16.0.1' )
        dmzserver2 = self.addHost( 'dmzserver2', ip='172.16.0.102/12', mac='00:00:00:00:DD:02',
                           defaultRoute='via 172.16.0.1' )
                           
    # Add external users
        ext1 = self.addHost( 'ext1', ip='147.0.0.101/12', mac='00:00:00:00:EE:01',
                           defaultRoute='via 147.0.0.1' )
        ext2 = self.addHost( 'ext2', ip='147.0.0.102/12', mac='00:00:00:00:EE:02',
                           defaultRoute='via 147.0.0.1' )
        ext3 = self.addHost( 'ext3', ip='147.0.0.103/12', mac='00:00:00:00:EE:03',
                           defaultRoute='via 147.0.0.1' )
                           
    #Add all the links of the hosts
        for h, s in [ (s1u1, s1), (s1u2, s1), (dmzserver1, sDMZ), (dmzserver2, sDMZ), (s2u1, s2), (s2u2, s2), (ext1, sEXT), (ext2, sEXT), (ext3, sEXT), (s1, s2)]:
            self.addLink( h, s )


def run():
    topo = NetworkTopo()
    net = Mininet( topo=topo,
    		    controller=RemoteController('c0', protocols="OpenFLow13"),
                   waitConnected=True,
                   switch=OVSKernelSwitch,
                   )
    net.start()
    net[ 's1' ].cmd( 'route add -net 192.168.1.0/24 dev s1-eth4' )
    net[ 's2' ].cmd( 'route add -net 192.168.0.0/24 dev s2-eth4' )
    net[ 'r0' ].cmd( 'haproxy -db -f /etc/haproxy/haproxy.cfg &' )
    net[ 'dmzserver1' ].cmd( 'python3 -m http.server --directory ~/ 80 &' )
    net[ 'dmzserver2' ].cmd( 'python3 -m http.server 80 &' )
    time.sleep(1)
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    info( '*** Balancer listening:\n' )
    info( net[ 'r0' ].cmd( 'netstat -lntu' ) )
    info( '*** Routing Table on Switch 1:\n' )
    info( net[ 's1' ].cmd( 'route' ) )
    info( '*** Routing Table on Switch 2:\n' )
    info( net[ 's2' ].cmd( 'route' ) )
    info( '*** Status HTTP server 1:\n' )
    info( net[ 'r0' ].cmd( 'curl -I 172.16.0.101 | grep HTTP/1.0' ) )
    info( '*** Status HTTP server 2:\n' )
    info( net[ 'r0' ].cmd( 'curl -I 172.16.0.102 | grep HTTP/1.0' ) )
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
