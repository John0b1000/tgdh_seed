# file: TCPAgent.py
#

# description: this file contains the TCPAgent class
#

# import modules
#
import socket
import pickle

# class: TCPAgent
#
class TCPAgent:

    # constructor
    #
    def __init__(self, port=9000, server=None):

        # define initial data
        # 
        self.PORT = port  # the TCP port for communication
        self.SERVER = server  # the listening server
        self.ADDR = (self.SERVER, self.PORT)  # socket variable

    #
    # end constructor

    # method: HandleClient
    #
    def HandleClient(self, connection, addr):

        # we must ensure that we can receive a large tree
        #
        LENGTH = 1000000

        # print the message (handle client protocol)
        #
        print(f"New connection - {addr}")
        connected = True
        while connected:
            tree = pickle.loads(connection.recv(LENGTH))
            print("\nTree object received!\n")
            connected = False
        connection.close()
        print(f"Connection closed - {addr}")
        return(tree)

    #
    # end method: HandleClient
    
    # method: ServerInit
    #
    def ServerInit(self):

        # start the server
        #
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.ADDR)
        server_socket.listen()
        print("Initializing TCP server ...")
        print(f"TCP server is listening on {self.SERVER}")

        # accept messages and return the transmitted tree
        #
        (connection, addr) = server_socket.accept()
        tree = self.HandleClient(connection, addr)
        server_socket.close()
        return(tree)

    #
    # end method: ServerInit

    # method: ClientInit
    #
    def ClientInit(self, utree):

        # serialize the tree and send
        #
        pickle_tree = pickle.dumps(utree)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.ADDR)
        client_socket.send(pickle_tree)

    #
    # end method: ClientInit

# 
# end class: TCPAgent

#
# end file: TCPAgent.py
