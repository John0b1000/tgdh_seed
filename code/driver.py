#!/usr/bin/env python3

# file: driver.py
#

# description: driver program for tgdh scheme
#

# version: 4
# 0: generating a simple tree structure given initial data
# 1: make a tree class to maintain nodes
# 2: use inheritance to organize the node class
# 3: add functionality: TypeAssign method, IDAssign method, FindMe method
# 4: add functionality: join event, leave event, post-run command line instructions; incorporate more built-in anytree functions
#

# usage:
#  python3 driver.py -s <initial size> -i <unique member ID>

# import modules
#
import sys
from functs import cmdl_parse, get_instructions
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

    # print the initial tree
    #
    btree.TreeExport()
    #btree.TreePrint()
    #btree.VerboseNodePrint()

    # wait for instructions from the commmand line
    #
    ex = get_instructions(btree)

    # exit gracefully
    #
    if ex == True:
        return(0)

#
# end function: main

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end file: driver.py
