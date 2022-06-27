# file: MulticastAgent.py
#

# description: a portable multicast class that can be used to send and receive messages
#

# import modules 
#
import socket
import struct

# class: MulticastAgent
#

class MulticastAgent:

    # constructor
    #
    def __init__(self, groups, port, iface=None, bind_group=None, mcast_group=None):
        
        # set class data
        #
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.groups = groups
        self.port = port
        self.iface = iface
        self.bind_group = bind_group
        self.mcast_group = mcast_group
        self.key_data = {'name':'key'}
    
    #
    # end constructor

    # method: recv
    #
    def recv(self):
        
        # allow reuse of socket 
        #
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind to groups
        #
        self.sock.bind(('' if self.bind_group is None else self.bind_group, self.port))
        for group in self.groups:
            mreq = struct.pack(
                '4sl' if self.iface is None else '4s4s',
                socket.inet_aton(group),
                socket.INADDR_ANY if self.iface is None else socket.inet_aton(self.iface))

            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # receive data
        #
        print("Receiving messages multicast to group {0}".format(self.bind_group))
        while True:

            # write the data to a file based on what was received
            #
            data = self.sock.recv(10240)
            parts = data.decode().split('/')
            if parts[1] == 'join':
                f = open("/files/events.txt", 'w', encoding='utf8')
                msg_contents = msg_contents = parts[1] + '/' + parts[2] + '\n'
                f.write(msg_contents)
                f.close()
            elif parts[1] == 'leave':
                f = open("/files/events.txt", 'w', encoding='utf8')
                msg_contents = msg_contents = parts[1] + '/' + parts[2] + '\n'
                f.write(msg_contents)
                f.close()
            else:
                if not (parts[1] in self.key_data):
                    self.key_data[parts[1]] = parts[2]
                    f = open("/files/keys.txt", 'a', encoding='utf8')
                    msg_contents = parts[1] + '/' + self.key_data[parts[1]] + '\n'
                    f.write(msg_contents)
                    f.close()
                elif parts[1] in self.key_data and not parts[2] == self.key_data[parts[1]]:
                    self.key_data[parts[1]] = parts[2]
                    f = open("/files/keys.txt", 'a', encoding='utf8')
                    msg_contents = parts[1] + '/' + self.key_data[parts[1]] + '\n'
                    f.write(msg_contents)
                    f.close()
                    
    #
    # end method: recv

    # method: send
    #
    def send(self, data):

        # bind to group
        #
        MULTICAST_TTL = 20
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        # send the data
        #
        self.sock.sendto(b'from MulticastAgent.py: ' + f'group: {self.mcast_group}, port: {self.port}, msg: {data}'.encode(), (self.mcast_group, self.port))

    #
    # end method: send

    # method: close
    #
    def close(self):

        # close the socket
        #
        self.sock.close()

    #
    # end method: close

#
# end class: MulticastAgent

#
# end file: MulticastAgent.py
