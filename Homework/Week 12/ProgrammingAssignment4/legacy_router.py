'''
Ethan Herndon
Alvin Liang
Maria Leftheriotis
Mustafa Memon
Programming Assignment 4
CST 311

Description: A Python program that builds a 2 host network connected by a legacy router. It is made such that the two hosts can send packets to each other. 
//TODO
1.Need to make sure that the IPs are set up correctly
a. For the router  DONE
b. For both hosts  DONE
2.For the link interfaces reference the miniedit script and the linuxrouter script DONE

3.Correct Network Design which allows h1 to ping h2 and for h2 to be able to ping h1. Draw and submit the network design in pdf format with IPs of all interfaces labelled. Also label the hosts as h1 and h2 and the switch as S/R. DONE
//

Document what changes you made to modify legacy_router.py and why those changes were made.

The 2 host need to be from 2 different subnets

Need to make sure that the IPs are set up correctly
For the router 
For both hosts
For the link interfaces
Reference the miniedit script and the linuxrouter script

'''
#!/usr/bin/python
# File: legacy_router.py
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

# setup network
def myNetwork():
    net = Mininet(topo=None,
                  build=False, ipBase='192.168.1.1/24') #There will be problems with the IPs ##UPDATE## IP changed

    info('*** Adding controller\n')
    info('*** Add switches\n')
    #Add the Router
    r1 = net.addHost('r1', cls=Node)
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')
    
    h1 = net.addHost('h1', ip='192.168.1.100/24',
                     defaultRoute='via 192.168.1.1') #NotGiven##UPDATE## both IPs dervied from ipBase  
    h2 = net.addHost('h2', ip='172.16.0.100/12',
                     defaultRoute='via 172.16.0.1') #UPDATED

    info('*** Add links\n')
    #REFERENCE=>
    #http://mininet.org/api/classmininet_1_1net_1_1Mininet.html
    net.addLink(h1, r1, intfName2='eth1-r1',
                params2={'ip': '192.168.1.1/24'})
    #Add a link from host 2 to router 2 to the interface
    net.addLink(h2, r1, intfName2='eth2-r1',
                params2={'ip': '172.16.0.1/12'})

    #Start the network
    info('*** Starting network\n')
    net.build()

    #Starting the Controller
    # added the following 5 lines of code:
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')

    info('*** Post configure switches and hosts\n')
    #Stop the network
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    #Runs the metho myNetwork
    myNetwork()
    # added 2 lines of code below:
    info('*** Routing Table on Router:\n')
    #Prints the routing table
    print net['r1'].cmd('route')

'''Expected result bfr edit

mininet@mininet-vm:~$ sudo python legacy_router.py
*** Adding controller
*** Add switches
*** Add hosts
*** Add links
*** Starting network
*** Configuring hosts
r1 h2 h1
*** Starting CLI:
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
From 10.0.0.1 icmp_seq=1 Destination Host Unreachable
From 10.0.0.1 icmp_seq=2 Destination Host Unreachable
From 10.0.0.1 icmp_seq=3 Destination Host Unreachable


'''