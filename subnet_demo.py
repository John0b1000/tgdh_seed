#!/usr/bin/env python3
# encoding: utf-8

###############################################################################
# import libraries
#
from seedemu.layers import Base, Routing, Ebgp
from seedemu.services import WebService
from seedemu.compiler import Docker
from seedemu.core import Emulator, Binding, Filter

###############################################################################
# function: add_customized_software(node_a)
#
def add_customized_software(node_a):

    # install Python3 and related files
    #
    node_a.addSoftware('python3')
    node_a.addSoftware('python3-dev').addSoftware('libssl-dev')
    node_a.addSoftware('python3-pip')

    # load the proper libraries
    #
    node_a.addBuildCommand('pip3 install pycryptodome py2p')
    node_a.addBuildCommand('pip3 install anytree')

    # install git, telnet, tmux, graphviz
    #
    node_a.addSoftware('git').addSoftware('telnet').addSoftware('tmux').addSoftware('graphviz')

    # add the proper directories
    #
    node_a.addBuildCommand('mkdir /files').addBuildCommand('touch /files/keys.txt').addBuildCommand('touch /files/events.txt')

    # grab the files
    #
    node_a.addSharedFolder('/tgdh_node', '../tgdh_node')
    
###############################################################################

# Initialize the emulator and layers
#
emu     = Emulator()
base    = Base()
routing = Routing()
ebgp    = Ebgp()
web     = WebService()

###############################################################################
# Create an Internet Exchange
#
base.createInternetExchange(100)

###############################################################################
# Create and set up AS-150
#

# Create an autonomous system
#
as150 = base.createAutonomousSystem(150)

# Create a network
#
as150.createNetwork('net0')

# Create a router and connect it to two networks
#
as150.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

# Create a host called web and connect it to a network
#
as150.createHost('web').joinNetwork('net0')

# Create a web service on virtual node, give it a name
# This will install the web service on this virtual node
#
web.install('web150')

# Create two new hosts for p2p TGDH communication exhibit
#
soldier1 = as150.createHost('soldier1').joinNetwork('net0')
soldier2 = as150.createHost('soldier2').joinNetwork('net0')
soldier3 = as150.createHost('soldier3').joinNetwork('net0')
soldier4 = as150.createHost('soldier4').joinNetwork('net0')
soldier5 = as150.createHost('soldier5').joinNetwork('net0')

# Add custom software to these two new nodes
#
add_customized_software(soldier1)
add_customized_software(soldier2)
add_customized_software(soldier3)
add_customized_software(soldier4)
add_customized_software(soldier5)

# Bind the virtual node to a physical node
#
emu.addBinding(Binding('web150', filter = Filter(nodeName = 'web', asn = 150)))

###############################################################################
# Create and set up AS-151
# It is similar to what is done to AS-150
#

as151 = base.createAutonomousSystem(151)
as151.createNetwork('net0')
as151.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as151.createHost('web').joinNetwork('net0')
web.install('web151')
emu.addBinding(Binding('web151', filter = Filter(nodeName = 'web', asn = 151)))

###############################################################################
# Create and set up AS-152
# It is similar to what is done to AS-150
#

as152 = base.createAutonomousSystem(152)
as152.createNetwork('net0')
as152.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')

as152.createHost('web').joinNetwork('net0')
web.install('web152')
emu.addBinding(Binding('web152', filter = Filter(nodeName = 'web', asn = 152)))

###############################################################################
# Peering these ASes at Internet Exchange IX-100
#

ebgp.addRsPeer(100, 150)
ebgp.addRsPeer(100, 151)
ebgp.addRsPeer(100, 152)

###############################################################################
# Rendering
#

emu.addLayer(base)
emu.addLayer(routing)
emu.addLayer(ebgp)
emu.addLayer(web)

emu.render()

###############################################################################
# Compilation
#

emu.compile(Docker(), './output')
