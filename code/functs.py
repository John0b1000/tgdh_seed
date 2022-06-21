# file: functs.py
#

# description: contains functions for tgdh driver program
#

# import modules
#
import argparse

# function: cmdl_parse
#
def cmdl_parse(alist):
    
    # parse the command line arguments
    #
    parser = argparse.ArgumentParser(description='Generate a Binary Key Tree')
    parser.add_argument('-s', metavar='isize', type=int, required=True, help='the initial size of the group')
    parser.add_argument('-i', metavar='m_id', required=True, help='unique member id')
    args = parser.parse_args(alist)

    # return in a tuple
    #
    return(int(args.s), int(args.i))

#
# end function: cmdl_parse

# function: get_instructions
#
def get_instructions(btree):

    # receive command line input
    #
    while True:
        instruct = input("Enter event here: ")
        if instruct == "join" or instruct == "j":
            btree.JoinEvent()
            btree.TreeExport() 
        elif instruct == "leave" or instruct == "l":
            lmem = int(input("Enter leaving member ID: "))
            print("Member " + str(lmem) + " is leaving ...")
            btree.LeaveEvent(lmem)
            btree.TreeExport()
        elif instruct == "q" or instruct == "quit":
            print("Freeing resources and exiting ...")
            return(True)  # exit gracefully
        elif instruct == "f" or instruct == "find":
            ans = input("Would you like to find a member or node? ")
            if ans == "m" or ans == "member":
                iden = input("Enter the member ID: ")
                fmem = btree.FindNode(iden, True)
                fmem.PrintAttributes()
            elif ans == "n" or ans == "node":
                iden = input("Enter node index (l,v): ")
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
            btree.TreeExport()
        else:
            print("**> Error: Invald input!")

#
# end function: get_instructions

#
# end file: functs.py
