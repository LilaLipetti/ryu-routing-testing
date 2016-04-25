#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch, OVSBridge
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='1.100.53.3',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')    
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='172.16.10.10/24', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='172.16.40.10/24', defaultRoute=None)
    

    info( '*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s3, s4)
    net.addLink(s2, s4)
        
    net.addLink(h1, s1)
    net.addLink(h2, s4)
     

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    
    info( '*** Add default routes to hosts \n')
    h1.cmd('ip route add default via 172.16.10.1')      
    h2.cmd('ip route add default via 172.16.40.1')
    
    
    info( '*** Post configure switches and hosts\n')
    info( '*** Switches should listen OpenFlow 1.3 commands \n')
    c0.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    c0.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    c0.cmd('ovs-vsctl set Bridge s3 protocols=OpenFlow13')
    c0.cmd('ovs-vsctl set Bridge s4 protocols=OpenFlow13')
        
    
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

