from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet

class ProjectTopo(Topo):
    def __init__(self):
 	#Initialize topology
	Topo.__init__(self)
	
        # Add hosts
	subnet1_user1 = self.addHost('sub1u1',ip='10.0.1.1') 
	subnet1_user2 = self.addHost('sub1u2',ip='10.0.1.2')
	subnet2_user1 = self.addHost('sub2u1',ip='10.0.2.1')
	subnet2_user2 = self.addHost('sub2u2',ip='10.0.2.2')
        
	# Add DMZ servers
	dmz_server1 = self.addHost('dmzserver1',ip='10.0.3.1')
	dmz_server2 = self.addHost('dmzserver2',ip='10.0.3.2')
	
	# Add external users
	external_user1 = self.addHost('ex1',ip='10.0.4.1')
	external_user2 = self.addHost('ex2',ip='10.0.4.2')
	external_user3 = self.addHost('ex3',ip='10.0.4.3')

	# Add  switches
	s1 = self.addSwitch('s1')
	s2 = self.addSwitch('s2')

	# For the r1 to the S1 and S2 and S1 to S2
	self.addLink(s1, s2) 

	# Add (bidirectional) links 
	# For the r1 to the external_users
	self.addLink(s1, external_user1)
	self.addLink(s2, external_user1)
	self.addLink(s1, external_user2)
	self.addLink(s2, external_user2)
	self.addLink(s1, external_user3)
	self.addLink(s2, external_user3)
	
	
	# For the S1 to h1 and h2
	self.addLink(s1, subnet1_user1)
	self.addLink(s1, subnet1_user2)
	
	# For the S2 to h3 and h4
	self.addLink(s2, subnet2_user1)
	self.addLink(s2, subnet2_user2)
	
	# For the S1 and S2 to DMZ
	self.addLink(s1, dmz_server1)
	self.addLink(s1, dmz_server2)
	
	self.addLink(s2, dmz_server1)
	self.addLink(s2, dmz_server2)    


# Adding the 'topos' dict with a key/value pair to
# generate our newly defined topology enables one
# to pass in '--topo=mytopo' from the command line.
topos = {'ProjectTopo': (lambda: ProjectTopo())}
