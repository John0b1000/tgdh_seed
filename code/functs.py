# file: functs.py
#

# description: contains functions for tgdh driver program
#

# import modules
#
import sys
import os
import argparse
from MulticastAgent import MulticastAgent
from TCPAgent import TCPAgent
from time import sleep

# function: cmdl_parse
#
def cmdl_parse(alist):
    
    # parse the command line arguments
    #
    parser = argparse.ArgumentParser(description='Generate a Binary Key Tree')
    parser.add_argument('-s', metavar='isize', type=int, help='the initial size of the group')        
    parser.add_argument('-i', metavar='uid', type=int, help='unique member id')
    parser.add_argument('-j', metavar='join', default=False, help='indicate a joining member')
    parser.add_argument('-a', metavar='ip_addr', help='IP address of current node')
    if len(alist) == 0:
        print("**> Error: Insufficient number of arguments specified.")
        parser.print_help(sys.stderr)        
        sys.exit(1)
    else:
        args = parser.parse_args(alist)

    # return in a tuple
    #
    return(args.s, args.i, args.j, args.a)

#
# end function: cmdl_parse

# function: get_instructions
#
def get_instructions(btree):

    # receive command line input
    #
    while True:
        print("########################################")
        instruct = input(">> Enter event here: ")
        print("########################################")
        if instruct == "join" or instruct == "j":
            btree.JoinEvent() 
        elif instruct == "leave" or instruct == "l":
            lmem = int(input(">> Enter leaving member ID: "))
            print("\tMember " + str(lmem) + " is leaving ...")
            print("---------------//---------------")
            btree.LeaveEvent(lmem)
        elif instruct == "q" or instruct == "quit":
            print("Freeing resources and exiting ...")
            return(True)  # exit gracefully
        elif instruct == "f" or instruct == "find":
            ans = input(">> Would you like to find a member or node? ")
            if ans == "m" or ans == "member":
                iden = input(">> Enter the member ID: ")
                fmem = btree.FindNode(iden, True)
                fmem.PrintAttributes()
            elif ans == "n" or ans == "node":
                iden = input(">> Enter node index (l,v): ")
                fnode = btree.FindNode(iden, False)
                fnode.PrintAttributes()
            else: print("**> Error: Invalid response!")
        elif instruct == "p" or instruct == "print":
            btree.TreePrint()
        elif instruct == "vp" or instruct == "verbose print":
            btree.TreePrint()
            btree.VerboseNodePrint()
        elif instruct == "u" or instruct == "update":
            btree.TreePrepEvent()
            btree.TreeRefresh()
        elif instruct == "pg" or instruct == "print_group_key":
            print("Group Key is: " + str(btree.root.key))
        else:
            print("**> Error: Invald input!")

#
# end function: get_instructions

# function: parse_config
#
def parse_config(line):

    # split the line into parts
    #
    parts = line.split('=')
    if parts[0] == 'groups':
        parts[1] = parts[1].split(',')
        parts[1] = [part.rstrip('\'').lstrip('\'') for part in parts[1]]
    else:
        parts[1] = parts[1].rstrip('\'').lstrip('\'')
    return(parts)

#
# end function: parse_config

# function: fread_config
#
def fread_config(fp):

    # read the file line by line using a buffer
    #
    mcast_params = {}
    for line in fp:
        line = line.rstrip('\n')
        if line != "[Settings]" and line != '\n':
            param = parse_config(line)
            mcast_params[param[0]] = param[1]
    return(mcast_params)
    
#
# end function: fread_config

# function: fread_keys
#
def fread_keys(fp):

    # read the file line by line using a buffer
    #
    for line in fp:
        line = line.rstrip('\n')
        return(line.split('/'))
    
#
# end function: fread_keys

# function: fread_events
#
def fread_events(fp):

    # read the file line by line using a buffer
    #
    for line in fp:
        line = line.rstrip('\n')
        parts = line.split('/')
        if parts[0] == 'join':
            return(1, parts[1])  # event code for join 
        elif parts[0] == 'leave':
            return(2, parts[1])  # event code for leave
        else:
            return(0, None)
    
#
# end function: fread_events

# function: clear_file
#
def clear_file(path):

    # clear a file with a specified path
    #
    f = open(path, 'w')
    f.close()

#
# end function: clear_file

# function: join_protocol
#
def join_protocol(ip_addr):

    # multicast a join message to the group
    #
    f = open("multicast.config", 'r', encoding='utf8')
    mcast_params = fread_config(f)
    f.close()
    mca = MulticastAgent(groups=mcast_params['groups'], port=int(mcast_params['port']), iface=mcast_params['iface'], bind_group=mcast_params['bind_group'], mcast_group=mcast_params['mcast_group'])
    print("---------------//---------------")
    print("Sending via multicast:\n\tJoining ... \n\tIP Address: {0}".format(ip_addr))
    msg = '/join/' + ip_addr
    mca.send(msg)
    print("---------------//---------------")

    # create TCP server and receive the tree object
    #
    print("---------------//---------------")
    tcpa = TCPAgent(server=ip_addr)
    return(tcpa.ServerInit())

#
# end function: join_protocol

# function: leave_protocol
#
def leave_protocol(btree):

    # multicast a leave message to the group
    #
    print("---------------//---------------")
    print("Sending via multicast:\n\tLeaving ... \n\tMember: {0}".format(btree.uid))
    msg = '/leave/' + str(btree.uid)
    btree.mca.send(msg)
    print("---------------//---------------")

#
# end function: join_protocol

# function: event_check
#
def event_check():

    # read the events file and determine if a join or leave has occurred 
    #
    if not (os.stat("/files/events.txt").st_size == 0):
        f = open("/files/events.txt", 'r', encoding='utf8')
        (event_code, data) = fread_events(f)
        f.close()
        return(event_code, data)
    else:
        return(0, None)

#
# end function: event_check

# function: forever
#
def forever(btree):

    try:

        # continually check for group membership events
        #
        print("Waiting for event ... ")
        while True:
            sleep(5)
            (event, data) = event_check()
            if event == 1:
                btree.JoinEvent(data)           
                btree.TreePrint()
                print("Group key: {0}".format(btree.root.key))
                clear_file("/files/events.txt")
                clear_file("/files/keys.txt")
                print("########################################")
                print("Waiting for event ...")
            elif event == 2:
                btree.LeaveEvent(int(data))
                btree.TreePrint()
                print("Group key: {0}".format(btree.root.key))
                clear_file("/files/events.txt")
                clear_file("/files/keys.txt")
                print("########################################")
                print("Waiting for event ...")

    except KeyboardInterrupt:

        # exit gracefully
        # 
        print("Leaving the group ...")
        print("Freeing resources and exiting ...")
        leave_protocol(btree)
        return(0)

#
# end file: functs.py
