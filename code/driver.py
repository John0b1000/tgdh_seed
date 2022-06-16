#!/usr/bin/env python3

# file: driver.py
#

# description: driver program for tgdh scheme
#

# sources: 
# https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
# https://anytree.readthedocs.io/en/latest/exporter/dotexporter.html
#

# version: 3
# 0: generating a simple tree structure given initial data
# 1: make a tree class to maintain nodes
# 2: use inheritance to organize the node class
# 3: add functionality: TypeAssign method, IDAssign method, FindMe method
#

# usage:
#  python3 driver.py -s <initial size> -i <unique member ID>

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
    #btree.root.PrintAttributes()
    btree.TreePrint()
    btree.TreeExport()

    # exit gracefully
    #
    return(0)

#
# end function: main

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end file: driver.py
