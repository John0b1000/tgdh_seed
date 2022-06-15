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
    return(args.s, args.i)

#
# end function: cmdl_parse

#
# end file: functs.py
