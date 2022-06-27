#!/usr/bin/env python3

# file: ListeningDaemon.py
#

# description: driver program for tgdh scheme
#

# import modules
#
import sys
from functs import fread_config, clear_file
from MulticastAgent import MulticastAgent

# function: main
#
def main(argv):

    # clear the keys.txt file and events.txt file
    #
    clear_file("/files/keys.txt")
    clear_file("/files/events.txt")

    # read the configuration file and determine multicast parameters
    #
    f = open("multicast.config", 'r', encoding='utf8')
    mcast_params = fread_config(f)
    f.close()

    # instantiate a listening object
    #
    mca = MulticastAgent(groups=mcast_params['groups'], port=int(mcast_params['port']), iface=mcast_params['iface'], bind_group=mcast_params['bind_group'], mcast_group=mcast_params['mcast_group'])

    try:

        # receive messages
        #
        mca.recv()

    finally:

        # exit gracefully
        #
        print("\nClosing ports and exiting...")               
        mca.close()
        return(0)

#
# end function: main
        
# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end of file