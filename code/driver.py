#!/usr/bin/env python3

# file: driver.py
#

# description: driver program for tgdh scheme
#

# version: 6
# 0: generating a simple tree structure given initial data
# 1: make a tree class to maintain nodes
# 2: use inheritance to organize the node class
# 3: add functionality: TypeAssign method, IDAssign method, FindMe method
# 4: add functionality: join event, leave event, post-run command line instructions; incorporate more built-in anytree functions; key generation
# 5: establish communication protocol; implement networking features
# 6: implement join and leave operations (single-member events)
#

# usage:
#  python3 driver.py -s <initial size> -i <unique member ID>

# import modules
#
import sys
from functs import cmdl_parse, get_instructions, join_protocol, clear_file, forever
from BinaryTree import BinaryTree

# function: main
#
def main(argv):

    # get command line arguments
    #
    (isize, uid, jstatus, ip_addr) = cmdl_parse(argv[1:len(argv)])

    if jstatus:

        # initiate join protocol
        #
        print("########################################")
        print("Joining the group ...")
        btree = join_protocol(ip_addr)
        btree.NewMemberProtocol()
        btree.TreePrint()
        print("Group key: {0}".format(btree.root.key))
        clear_file("/files/events.txt")
        clear_file("/files/keys.txt")
        print("########################################")

    else: 

        # instantiate a binary tree object
        #
        print("########################################")
        print("Initializing ...")
        btree = BinaryTree(size=isize, uid=uid)
        print("########################################")

    # check the events.txt file every few seconds
    #
    return(forever(btree))

#
# end function: main

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end file: driver.py
