# file: network_demo.py
#

# import modules
#
import sys
import time
from math import floor, log
from copy import copy
from osbrain import run_agent
from osbrain import run_nameserver
from tgdhstruct.tgdhstruct import TgdhStruct

# function: receive_bkeys
#
def receive_bkeys(agent, message):
    agent.log_info(f"Received: {message}")
    data = message.split(':')
    node = agent.data.btree.find_node(data[0].lstrip('<').rstrip('>'), False)
    node.b_key = int(data[1])
#
# end function: receive_bkeys

# function: receive_tree
#
def receive_tree(agent, tree):
    agent.log_info("Tree received!")
    agent.data = tree
#
# end function: receive_tree

# function: join_key_exchange
#
def join_key_exchange(agents_a, size_a, addr_a, spon_id_a, new_id_a):

    # define the initial size
    #
    size = size_a

    # create a variable to keep track of the current level
    #
    nodemax = (2*size)-1
    max_height = floor(log((nodemax-1),2))
    level = 1

    # get the update paths of all members
    #
    agents = agents_a
    addr = addr_a
    update_paths = []
    for i in range(size):
        if i not in (spon_id_a-1, new_id_a-1):
            temp_update_path = []
            for node in agents[i].data.btree.get_update_path():
                temp_update_path.append(node.name)
            update_paths.append(list(reversed(temp_update_path)))
        else:
            update_paths.append(None)

    # get the sponsor's key path
    #
    spon_key_path = []
    for node in agents[spon_id_a-1].data.btree.my_node.get_key_path():
        spon_key_path.append(node.name)
    
    while level < max_height:    

        # only the sponsor will publish
        #
        mem = f'mem_{spon_id_a}'
        addr[spon_id_a-1] = agents[spon_id_a-1].bind('PUB', alias=mem)

        # establish subscribers (sponsor will publish)
        #
        key_node = spon_key_path[level]
        for i in range(size):
            if update_paths[i] is not None:
                if key_node in update_paths[i]:
                    dest_name = key_node
                    if dest_name is not None:
                        agents[i].connect(addr[spon_id_a-1], handler=receive_bkeys)

        # sponsor sends appropriate blind keys
        #
        blind_key = agents[spon_id_a-1].data.btree.find_node(key_node.lstrip('<').rstrip('>'), False).b_key
        message = f'{key_node}:{blind_key}'
        print(f"\nMember {agents[spon_id_a-1].data.btree.uid} is sending keys ...\n")
        agents[spon_id_a-1].send(mem, message)

        # close connections to prevent unnecessary sending/receiving
        #
        for agent in agents:
            agent.close_all()

        time.sleep(1)
        print(f"\nLevel {max_height-level} finished!")
        level = level+1
#
# end function: join_key_exchange

# function: initial_key_exchange
#
def initial_key_exchange(agents_a, size_a, initflag):

    # define the initial size
    #
    size = size_a

    # create a variable to keep track of the current level
    #
    nodemax = (2*size)-1
    max_height = floor(log((nodemax-1),2))
    level = 0

    # initialize all agents with their trees and co-paths
    #
    agents = agents_a
    key_paths = []
    co_paths = []
    iters = [0]*size
    for i in range(size):
        mem = f'mem_{i+1}'
        if initflag:
            agents.append(run_agent(mem))
            agents[i].data = TgdhStruct(size, i+1)
        temp_key_path = []
        for node in agents[i].data.btree.my_node.get_key_path():
            temp_key_path.append(node.name)
        key_paths.append(temp_key_path)
        temp_co_path = []
        for node in agents[i].data.btree.my_node.get_co_path():
            temp_co_path.append(node.name)
        co_paths.append(temp_co_path)

    # pad the co-path lists to account for co-paths of varying lengths
    #
    for i in range(size):
        if len(co_paths[i]) < max_height:
            co_padding = [None]*(max_height-len(co_paths[i]))
            key_padding = [None]*(max_height-len(key_paths[i])+1)
            co_paths[i] = co_padding + co_paths[i]
            key_paths[i] = key_padding + key_paths[i]

    while level < max_height:    

        # establish publishers (each node will publish)
        #
        addr = []
        for i in range(size):
            mem = f'mem_{i+1}'
            addr.append(agents[i].bind('PUB', alias=mem))

        # establish subscribers (proper co-path member)
        #
        for i in range(size):
            dest_name = co_paths[i][level]
            if dest_name is not None:
                dest_node = agents[i].data.btree.find_node(dest_name.lstrip('<').rstrip('>'), False)
                dest_mem = dest_node.leaves[0].mid
                agents[i].connect(addr[dest_mem-1], handler=receive_bkeys)

        # send blind keys for the proper node
        #
        for i in range(size):
            mem = f'mem_{i+1}'
            key_node = key_paths[i][level]
            if key_node is not None:
                blind_key = agents[i].data.btree.find_node(key_node.lstrip('<').rstrip('>'), False).b_key
                message = f'{key_node}:{blind_key}'
                print(f"\nMember {agents[i].data.btree.uid} is sending keys ...\n")
                agents[i].send(mem, message)

        # calculate appropriate blind keys
        #
        time.sleep(1)
        for i in range(size):
            if co_paths[i][level] is not None:
                newtree = agents[i].data
                newtree.btree.initial_calculate_group_key(iters[i])
                iters[i] = iters[i]+1
                agents[i].data = newtree
                print(f"\n{'Tree Updation'.center(80, '-')}")
                agents[i].data.btree.tree_print()

            # close connections to prevent unnecessary sending/receiving
            #
            agents[i].close_all()

        time.sleep(1)
        print(f"\nLevel {max_height-level} finished!")
        level = level+1
    
    # return the addresses for a join or leave event
    #
    return(addr)
#
# end function: initial_key_exchange

# function: join_protocol
#
def join_protocol(agents_a, addr_a, size_a):
    
    # alert current members that a new member is joining; find the sponsor
    #
    agents = agents_a
    for i in range(size_a):
        newtree = agents[i].data
        newtree.btree.join_event()
        agents[i].data = newtree
        if agents[i].data.btree.my_node.ntype == 'spon':
            sponsor = agents[i]

    # initialize the joining member
    #
    mem = f'mem_{sponsor.data.btree.nextmemb-1}'
    agents.append(run_agent(mem))
    agents[-1].data = None

    # joining member subscribes to the sponsor
    #
    addr = addr_a
    mem = f'mem_{sponsor.data.btree.uid}'
    addr.insert(sponsor.data.btree.uid-1, sponsor.bind('PUB', alias=mem))
    dest_mem = sponsor.data.btree.uid
    agents[-1].connect(addr[dest_mem-1], handler=receive_tree)

    # sponsor sends the tree to the joining member
    #
    spon_id = sponsor.data.btree.uid
    stree = copy(sponsor.data)
    stree.btree.my_node.key = None
    print(f"\nMember {agents[spon_id-1].data.btree.uid} is sending the tree ...\n")
    sponsor.send(mem, stree)

    # allow new member to update its tree
    #
    time.sleep(1)
    newtree = agents[-1].data
    newtree.btree.new_member_protocol()
    agents[-1].data = newtree
    new_id = agents[-1].data.btree.uid

    # close connections
    #
    for agent in agents:
        agent.close_all()

    # new member shares blind key with sponsor
    #
    mem = f'mem_{agents[-1].data.btree.uid}'
    addr[-1] = agents[-1].bind('PUB', alias=mem)
    sponsor.connect(addr[-1], handler=receive_bkeys)
    blind_key = agents[-1].data.btree.my_node.b_key
    message = f'{agents[-1].data.btree.my_node.name}:{blind_key}'
    print(f"\nMember {agents[new_id-1].data.btree.uid} is sending keys ...\n")
    agents[-1].send(mem, message)

    # allow the sponsor and new member to calculate the group key
    #
    time.sleep(1)
    newtree_s = agents[spon_id-1].data
    newtree_s.btree.calculate_group_key()
    agents[spon_id-1].data = newtree_s
    print(f"\n{'Tree Updation'.center(80, '-')}")
    agents[spon_id-1].data.btree.tree_print()
    newtree_n = agents[-1].data
    newtree_n.btree.calculate_group_key()
    agents[-1].data = newtree_n
    print(f"\n{'Tree Updation'.center(80, '-')}")
    agents[-1].data.btree.tree_print()

    # resend all blind keys
    #
    print(f"\n{'Key Exchange (Join)'.center(80, '=')}")
    join_key_exchange(agents, size_a+1, addr, spon_id, new_id)

    # allow all remaining members to calculate the group key
    #
    time.sleep(1)
    for i in range(size_a+1):
        if i not in (spon_id-1, new_id-1):
            newtree = agents[i].data
            newtree.btree.calculate_group_key()
            agents[i].data = newtree
            print(f"\n{'Tree Updation'.center(80, '-')}")
            agents[i].data.btree.tree_print()

    # return the new size of the tree and the addresses
    #
    return(size_a+1, addr)
#
# end function: join_protocol

# function: main
#
def main(argv):

    # deploy the nameserver
    #
    ns = run_nameserver()

    # get the initial size
    #
    size = int(argv[1])

    # initialize the tree
    #
    print(f"\n{'Key Exchange (Init)'.center(80, '=')}")
    agents = []
    addr = initial_key_exchange(agents, size, True)
    print("\nTree initialization completed!\nAll initial members have computed the group key.")

    # test a join event
    #
    time.sleep(1)
    print(f"\n{'Join Event'.center(80, '=')}")
    size, addr = join_protocol(agents, addr, size)
    print(f"\n{'Join Event'.center(80, '=')}")
    size, addr = join_protocol(agents, addr, size)

    # close the system
    #
    print(f"\n{'Exiting Program'.center(80, '=')}\n")
    ns.shutdown()
#
# end function: main

# begin gracefully
#
if __name__ == '__main__':
    main(sys.argv)

#
# end file: network_demo.py