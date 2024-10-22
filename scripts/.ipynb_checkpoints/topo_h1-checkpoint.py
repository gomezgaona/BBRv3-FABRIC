#!/usr/bin/python

import os
import subprocess
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI

def start_mininet_hosts(num_hosts, buffer_size):
    if(num_hosts > 254):
        print("You are trying to add more than 254 senders and receivers")
        return
    net = Mininet(topo=None, build=False, ipBase='172.16.0.0/16')

    # Create switches
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    print("Creating switches")
    
    # Start hosts and connect them to the switch
    for i in range(1, num_hosts + 1):
        # Senders (hs)
        hs = net.addHost(f'hs{i}', ip=f'172.16.0.{i}/16')
        hs.cmd('sysctl -w net.ipv4.tcp_wmem="{} {} {}"'.format(buffer_size, buffer_size, buffer_size))
        hs.cmd('sysctl -w net.ipv4.tcp_rmem="{} {} {}"'.format(buffer_size, buffer_size, buffer_size))
        net.addLink(hs, s1)
        #print(i)
    print(f"Creating hosts, setting TCP send and receive buffers to {buffer_size}, and connecting hosts to the switches")

    # Start the network
    net.start()
    print("Starting the network")

    # Open the Mininet CLI
    net.interact()
    
    # Clean up after the network has been stopped
    # net.stop()

# Enter the number of hosts
num_hosts = 4
TCP_buffer_size = "4096 1000000 200000000"

start_mininet_hosts(num_hosts, TCP_buffer_size)


