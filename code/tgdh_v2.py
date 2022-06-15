#!/usr/bin/env python3

# file: tgdh_v2.py
#

# description: driver program for tgdh scheme
#

# version: 2
# 0: generating a simple tree structure given initial data
# 1: make a tree class to maintain nodes
# 2: use inheritance to organize the node class
#

# usage:
#  python3 tgdh_v2.py -s <initial size> -i <unique member ID>

# import modules
#
import sys
from functs import cmdl_parse
from BinaryTree import BinaryTree

# function: main
#
def main(argv):

    # get command line arguments
    #
    (isize, uid) = cmdl_parse(argv[1:len(argv)])

    # instantiate a binary tree object 
    #
    btree = BinaryTree(size=isize, uid=uid)

    # generate a graphic of the tree for visualization
    #
    btree.TreeExport()

#
# end function: main

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end file: tgdh_v2.py
