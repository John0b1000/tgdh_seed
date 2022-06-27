# file: BinaryTree.py
#

# description: contains the BinaryTree class
#

# import modules
#
import sys
from DataNode import DataNode
from functs import fread_config, fread_keys, clear_file
from MulticastAgent import MulticastAgent
from TCPAgent import TCPAgent
from anytree.exporter import DotExporter
from anytree import RenderTree
from anytree import search
from anytree import PreOrderIter
import math
import itertools
from copy import copy

# class: BinaryTree
#

class BinaryTree:

    # constructor
    #
    def __init__(self, size=2, uid=None):

        # define initial data
        #
        self.size = size  # number of members in the group
        self.uid = uid  # unique member ID
        self.me = None # the node in the tree that refers to me
        self.nodetrack = 1  # number of nodes generated
        self.nodemax = (2*size)- 1  # maximum number of nodes in a tree with self.size members
        self.nextmemb = size+1  # the member ID of the next member to join the tree 
        self.height = math.floor(math.log((self.nodemax-1),2))  # height of the tree
        self.root = DataNode() # root of the tree
        self.RefreshPath = None  # the path of keys that need to be updated after a join or leave
        self.mca = self.EstablishMulticast()  # a multicasting object used to send messages
        self.ip_addr_send = None  # the ip address to send the serial object when sponsor

        # build an initial tree and print it
        #
        self.BuildTree()

    #
    # end constructor

    # method: EstablishMulticast
    #
    def EstablishMulticast(self):

        # set up multicast communication
        #
        f = open("multicast.config", 'r', encoding='utf8')
        mcast_params = fread_config(f)
        f.close()
        return(MulticastAgent(groups=mcast_params['groups'], port=int(mcast_params['port']), iface=mcast_params['iface'], bind_group=mcast_params['bind_group'], mcast_group=mcast_params['mcast_group']))

    #
    # end method: EstablishMulticast

    # method: AddNodes
    #
    def AddNodes(self, curr_n):

        # add two nodes to keep the tree full
        #
        curr_n.lchild = DataNode(pos='left', l=curr_n.l+1, v=2*curr_n.v, parent=curr_n, ntype='inter')
        curr_n.rchild = DataNode(pos='right', l=curr_n.l+1, v=(2*curr_n.v)+1, parent=curr_n, ntype='inter')

    #
    # end method: AddNodes

    # method: GetLeaves
    #
    def GetLeaves(self):

        # return the leaves of the tree
        #
        return(self.root.leaves)

    #
    # end method: GetLeaves

    # method: WalkTreeBuild
    #
    def WalkTreeBuild(self, curr_n):

        # walk along the tree and add the appropriate nodes
        #
        if not curr_n.IsLeaf():
            self.WalkTreeBuild(curr_n.rchild)
            if self.nodetrack is not self.nodemax:
                self.WalkTreeBuild(curr_n.lchild)
        else:
            self.AddNodes(curr_n)
            self.nodetrack = self.nodetrack + 2  # nodes are added in pairs

    #
    # end method: WalkTreeBuild
    
    # method: WalkPreOrder
    #
    def WalkPreOrder(self, root):

        # traverse the tree in preorder fashion
        #
        return(PreOrderIter(root))

    #
    # end method: WalkPreOrer

    # method: TypeAssign
    #
    def TypeAssign(self):

        # traverse the tree and assign types to each node
        #
        for node in self.GetLeaves():
            node.ntype = 'mem'

    #
    # end method: TypeAssign

    # method: IDAssign
    #
    def IDAssign(self):

        # generate member ID lists
        #
        baselist = [1,2]
        if self.height >= 1:
            for i in range(0, self.height-1):
                templist = list(reversed(range(pow(2,i+2)+1)))
                newlist = templist[0:pow(2,i+1)]
                baselist = list(itertools.chain(*zip(baselist, newlist)))
        max_size = pow(2,self.height)
        hlist = list(reversed(range(max_size+1)))
        rm_nodes = hlist[0:max_size-self.size]
        for num in rm_nodes:
            baselist.remove(num)

        # assign the ID numbers
        # 
        idlist = list(reversed(baselist))
        c = len(baselist)-1
        for node in self.GetLeaves():
            node.mid = idlist[c]
            c = c-1
        
    #
    # end method: IDAssign

    # method: FindMe
    #
    def FindMe(self):

        # function: me_finder
        #
        def me_finder(node):

            # find me
            #
            if node.mid == self.uid:
                return(node)

        #
        # end function: me_finder

        # find the node that matches this members's unique ID
        #
        self.me = search.find(self.root, me_finder)

    #
    # end method: FindMe

    # method: KeyGeneration
    #
    def KeyGeneration(self):

        # generate the Diffie-Hellman keys for my node only
        #
        self.me.GenPrivateKey()
        self.me.GenBlindKey()

    #
    # end method: KeyGeneration

    # method: GetKey
    #
    def GetKey(self, name):

        # wait for the key to be added to the file
        #
        print("---------------//---------------")
        print("Receiving via multicast ...")
        f = open("/files/keys.txt", 'r', encoding='utf8')
        while True:
            data = fread_keys(f)
            if data is not None:
                if data[0] == name:
                    f.close()
                    (print("\tBlind key: {0}\n\tFor node: {1}".format(data[1], data[0])))
                    print("---------------//---------------")
                    return(int(data[1]))

    #
    # end method: GetKey

    # method: SendKey
    #
    def SendKey(self, node):

        # multicast this blind key to the rest of the group
        #
        print("---------------//---------------")
        msg = '/' + node.name + '/' + str(node.bKey)
        print("Sending via multicast:\n\tBlind key: {0}\n\tFor node: {1}".format(node.bKey, node.name))
        self.mca.send(msg)
        #print("UDP packet structure: [ {0} | {1} ]".format(node.name, node.bKey))
        print("---------------//---------------")

    #
    # end method: SendKey

    # method: InitialCalculateGroupKey
    #
    def InitialCalculateGroupKey(self):

        # traverse to the root and calculate the group key; send the blind keys
        #
        key_path = self.me.GetKeyPath()
        co_path = self.me.GetCoPath()
        self.SendKey(self.me)
        for i, node in enumerate(co_path):
            node.bKey = self.GetKey(node.name)
            key_path[i+1].key = pow(int(node.bKey), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].GenBlindKey()
                self.SendKey(key_path[i+1])

        # clear the keys file now that they are all in memory
        #
        clear_file("/files/keys.txt")

    #
    # end method: InitialCalculateGroupKey

    # method: SponsorCalculateSendGroupKey
    #
    def SponsorCalculateSendGroupKey(self):

        # traverse to the root and calculate the group key
        #
        key_path = self.me.GetKeyPath()
        co_path = self.me.GetCoPath()
        self.SendKey(self.me)
        for i, node in enumerate(co_path):
            key_path[i+1].key = pow(int(node.bKey), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].GenBlindKey()
                self.SendKey(key_path[i+1])

    # 
    # end method: SponsorCalculateSendGroupKey

    # method: CalculateGroupKey
    #
    def CalculateGroupKey(self):

        # traverse to the root and calculate the group key
        #
        key_path = self.me.GetKeyPath()
        co_path = self.me.GetCoPath()
        for i, node in enumerate(co_path):
            key_path[i+1].key = pow(int(node.bKey), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].GenBlindKey()

    # 
    # end method: CalculateGroupKey

    # method: BuildTree
    #
    def BuildTree(self):

        # build the tree
        #
        print("---------------//---------------")
        print("Generating Tree with {0} members ...".format(str(self.size).rjust(2)))
        print("I am member {0}".format(str(self.uid).rjust(2)))
        print("---------------//---------------")
        while self.nodetrack is not self.nodemax:
            self.WalkTreeBuild(self.root)

        # set node attributes
        #
        self.TypeAssign()
        self.IDAssign()
        self.FindMe()
        self.KeyGeneration()
        self.TreeExport()
        self.InitialCalculateGroupKey()
        self.TreePrint()
        print("Group key: {0}".format(self.root.key))

    #
    # end method: BuildTree

    # method: FindNode
    #
    def FindNode(self, iden, memflag):

        # function: mem_finder
        #
        def mem_finder(node):

            # find member
            #
            if node.mid == int(iden):
                return(node)

        #
        # end function: mem_finder

        # function: node_funder
        #
        def node_finder(node):

            # find any node
            #
            if str(node.l) + ',' + str(node.v) == iden:
                return(node)
            
        #
        # end function: node_finder

        # find a specific node by member number or index
        #
        if memflag == True:
            return(search.find(self.root, mem_finder))
        else:
            return(search.find(self.root, node_finder))

    # 
    # end method: FindNode

    # method: RecalculateNames
    #
    def RecalculateNames(self):

        # recalculate all names in the tree
        #
        for node in self.WalkPreOrder(self.root):
            node.name = node.CalculateName()
    
    # 
    # end method: RecalculateNames

    # method: FindInsertion
    #
    def FindInsertion(self):

        # find the shallowest level
        #
        llist = []
        plist = []
        for node in self.GetLeaves():
            llist.append(node.l)
            plist.append(node)
        slevel = min(llist)

        # find the rightmost node on the shallowest level with no children
        #
        slist = [node for node in plist if node.l == slevel]
        olist = [node for node in slist if node.IsLeaf()]
        return(olist[len(olist)-1])

    #
    # end method: FindInsertion

    # method: SponsorCommProtocol
    #
    def SponsorCommProtocol(self, node=None, join=True):

        # the sponsor must send out the updated blind keys
        #

        # if this is a join, send the serialized tree and get the blind key from the new member
        #
        if join:
            print("---------------//---------------")
            print("Serializing and sending tree ...")
            tcpa = TCPAgent(port=9000, server=self.ip_addr_send)
            send_tree = copy(self)
            tempkeys = [self.me.key, self.me.bKey]
            send_tree.me.key = None
            send_tree.me.bKey = None
            send_tree.mca = None
            tcpa.ClientInit(send_tree)
            self.me.key = tempkeys[0]
            self.me.bKey = tempkeys[1]
            node.bKey = self.GetKey(node.name)
            self.SponsorCalculateSendGroupKey()
            self.CalculateGroupKey()
        else:

            # otherwise, just calculate and send (sponsor calculates new private key)
            #
            print("---------------//---------------")
            print("Generating new keys ...")
            self.KeyGeneration()
            print("---------------//---------------")
            self.SponsorCalculateSendGroupKey()

    #
    # end method: SponsorCommProtocol

    # method: GrabUpdatedKeys
    #
    def GrabUpdatedKeys(self):

        # determine which keys need to be updated after a join or leave event
        #
        new_path = set(self.RefreshPath)
        our_path = set(self.me.GetCoPath())
        for node in our_path.intersection(new_path):
            node.bKey = self.GetKey(node.name)

    #
    # end method: GrabUpdatedKeys

    # method: EmptyCheck
    #
    def EmptyCheck(self):

        # determine if I am the only one left in the group; if so, exit
        #
        if self.root.lchild.IsLeaf() and self.root.rchild.IsLeaf():
            print("---------------//---------------")
            print("This group is empty! Program will terminate.")
            print("---------------//---------------")
            sys.exit(0)

    #
    # end method: EmptyCheck

    # method: TreePrepEvent
    #
    def TreePrepEvent(self):

        # prepare the tree for a join or leave event
        #
        self.TypeAssign()

    #
    # end method: TreePrepEvent

    # method: TreeRefresh
    #
    def TreeRefresh(self, event='u', ip_addr_send=None):

        # refresh appropriate tree attributes
        #
        self.FindMe()
        self.RecalculateNames()
        self.TreeExport()
        if self.me.ntype != 'spon':
            self.GrabUpdatedKeys()
            self.CalculateGroupKey()
        else:
            print("---------------//---------------")
            print("I am the sponsor!")
            print("Entering sponsor protocol ...")
            print("---------------//---------------")
            if event == 'j':
                self.ip_addr_send = ip_addr_send
                self.SponsorCommProtocol(node=self.me.GetSibling(), join=True)
            else:
                self.SponsorCommProtocol(join=False)

    #
    # end method: TreeRefresh

    # method: JoinEvent
    #
    def JoinEvent(self, ip_addr_send=None):

        # prepare the tree
        #
        self.TreePrepEvent()

        # create two new nodes at the insertion node
        #
        inserti_node = self.FindInsertion()
        self.AddNodes(inserti_node)
        sponsor_node = inserti_node.lchild  # the sponsor is always the sibling of the new member
        newmemb_node = inserti_node.rchild
        self.RefreshPath = newmemb_node.GetKeyPath()

        # assign types, IDs, and keys
        #
        sponsor_node.SponsorAssign(mid=inserti_node.mid, key=inserti_node.key, bKey=inserti_node.bKey, join=True) 
        inserti_node.InsertionAssign()
        newmemb_node.NewMembAssign(self.nextmemb)

        # signal that a new member has been added
        #
        self.nextmemb = self.nextmemb+1

        # refresh the tree
        #
        self.TreeRefresh(event='j', ip_addr_send=ip_addr_send)

    #
    # end method: JoinEvent

    # method: LeaveEvent
    #
    def LeaveEvent(self, eid):

        # prepare the tree
        #
        self.EmptyCheck()
        self.TreePrepEvent()

        # find the member to be erased
        #
        for node in self.GetLeaves():
            if node.mid == eid:

                if node.parent.ntype == 'root':

                    # the root must be relocated
                    #
                    new_root = node.GetSibling()
                    new_root.MakeRoot()
                    self.root = new_root
                    sponsor_node = list(self.WalkPreOrder(self.root))[-1]
                    sponsor_node.SponsorAssign(join=False)

                else:

                    # assign the sponsor
                    #
                    sponsor_node = list(self.WalkPreOrder(node.GetSibling()))[-1]
                    sponsor_node.SponsorAssign(join=False)

                    # transfer data from the sibling node to the parent
                    # the parent node is being replaced
                    #
                    node.parent.TransferDataRemove(node.GetSibling())

        self.RefreshPath = self.FindNode(sponsor_node.mid, True).GetKeyPath()

        # refresh the tree
        #
        self.TreeRefresh(event='l')

    #
    # end method: LeaveEvent

    # method: NewMemberProtocol
    #
    def NewMemberProtocol(self):

        # establish a multicast connection
        #
        self.mca = self.EstablishMulticast()

        # find me
        #
        self.uid = self.nextmemb-1
        self.FindMe()

        # generate keys and multicast blind key
        #
        print("---------------//---------------")
        print("Generating new keys ...")
        self.KeyGeneration()
        print("---------------//---------------")
        self.SendKey(self.me)
        
        # get the blind key from the sponsor
        #
        self.me.GetSibling().bKey = self.GetKey(self.me.GetSibling().name)

        # calculate the group key
        #
        self.CalculateGroupKey()

    #
    # end method: NewMemberProtocol

    # method: TreeExport
    #
    def TreeExport(self):

        # function: nodeattrfunc
        #
        def nodeattrfunc(node):

            # label the node that is me
            #
            if node == self.me:
                return('label="%s\n%s: %s (me)"' % (node.name, node.ntype, node.mid))
            elif node.mid is not None:
                return('label="%s\n%s: %s\n"' % (node.name, node.ntype, node.mid))
            else:
                return('label="%s\n%s"' % (node.name, node.ntype))
        
        #
        # end function: nodeattrfunc
        
        # use graphics module to print tree 
        #
        DotExporter(self.root, nodeattrfunc=nodeattrfunc).to_picture("TreeExport.png")

    #
    # end method: TreeExport

    # method: TreePrint
    #
    def TreePrint(self):

        # print the tree via the terminal
        #
        print("---------------//---------------")
        print("Displaying tree ...")
        for pre, _, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            datastr = u"type: %s, ID: %s, key: %s, bKey: %s" % (node.ntype, node.mid, node.key, node.bKey)
            print(treestr.ljust(8), datastr)
        print("---------------//---------------")
        
    #
    # end method: TreePrint

    # method: VerboseNodePrint
    #
    def VerboseNodePrint(self):

        # print each attribute for every node
        #
        for node in self.WalkPreOrder(self.root):
            node.PrintAttributes()

    #
    # end method: VerboseNodePrint

#
# end class: BinaryTree

#
# end file: BinaryTree.py
