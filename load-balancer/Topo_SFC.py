
from mininet.topo import Topo

class Topo_SFC(Topo):
    def __init__(self):
        Topo.__init__(self)

        s1 = self.addSwitch('s1', dpid="0000000000000001")
        s2 = self.addSwitch('s2', dpid="0000000000000002")
        s3 = self.addSwitch('s3', dpid="0000000000000003")

        self.addLink(s1, s3, port1=1, port2=1)
        self.addLink(s1, s2, port1=2, port2=1)
        self.addLink(s2, s3, port1=2, port2=2)

        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        server1 = self.addHost('server1', ip='10.0.0.11/24')
        server2 = self.addHost('server2', ip='10.0.0.12/24')

        self.addLink(s1, h1, port1=11)
        self.addLink(s1, h2, port1=12)
        self.addLink(s3, server1, port1=11)
        self.addLink(s3, server2, port1=12)

topos = { 'topo_SFC': ( lambda: Topo_SFC() ) }
