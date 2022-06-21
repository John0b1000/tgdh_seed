# file: DataNode.py
#

# description: contains the DataNode class
#

# import modules
#
from anytree import NodeMixin
from Crypto.Random.random import randint

# class: DataNode
#

class DataNode(NodeMixin):

    # define global Diffie-Hellman Data (2048-bit)
    #
    g = 2
    #p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    p = 7  # small number for decoding purposes

    # constructor
    #
    def __init__(self, pos='NA', l=0, v=0, parent=None, ntype='root', mid=None, rchild=None, lchild=None):

        # define class data
        #

        # tree data
        #
        self.pos = pos
        self.l = l  # level index
        self.v = v  # position index
        self.parent = parent  # parent of the node
        self.ntype = ntype  # node type: root, inter, member, sponsor
        self.mid = mid  # member ID
        self.rchild = rchild  # right child of the node 
        self.lchild = lchild  # left child of the node
        self.name = self.CalculateName()  # index value (used as name attribute for graphic generation)

        # Diffie-Hellman encryption data
        #
        self.key = None  # randomly generated private key
        self.bKey = None   # blind (public) key

    #
    # end constructor

    # method: IsLeaf
    #
    def IsLeaf(self):

        # determine if this node is a leaf
        #
        return(self.is_leaf)
    
    #
    # end method: IsLeaf

    # method: GetSiblings
    #
    def GetSibling(self):

        # return the sibling of the tree
        # this is a binary tree structure so each node has only one sibling
        #
        return(self.siblings[0])

    # 
    # end method: GetSiblings

    # method: CalculateName
    #
    def CalculateName(self):

        # update location variables and determine my name
        #
        if self.pos == 'left':
            self.l = self.parent.l+1
            self.v = 2*self.parent.v
            return('<' + str(self.l) + ',' + str(self.v) + '>')
        elif self.pos == 'right':
            self.l = self.parent.l+1
            self.v = 2*self.parent.v+1
            return('<' + str(self.l) + ',' + str(self.v) + '>')
        else: 
            return('<' + str(self.l) + ',' + str(self.v) + '>')

    #
    # end method: CalculateName

    # method: GenPrivateKey
    #
    def GenPrivateKey(self):

        # generate the private key
        #
        return(randint(1, int(DataNode.p-1)))

    # 
    # end method: GenPrivateKey

    # method: GenBlindKey
    #
    def GenBlindKey(self):

        # generate the blind key
        #
        return(pow(DataNode.g, self.key, DataNode.p))

    #
    # end method: GenBlindKey

    # method: SponsorAssign
    #
    def SponsorAssign(self, mid=0, join=True):
        
        # assign data 
        #
        self.ntype = 'spon'
        if join == True:
            self.mid = mid

    #
    # end method: SponsorAssign

    # method: InsertionAssign
    #
    def InsertionAssign(self):

        # assign data
        #
        self.ntype = 'inter'
        self.mid = None

    #
    # end method: InsertionAssign
    
    # method: NewMembAssign
    #
    def NewMembAssign(self, mid):
        
        # assign data
        #
        self.ntype = 'mem'
        self.mid = mid

    #
    # end method: NewMembAssign

    # method: TransferData
    #
    def TransferDataRemove(self, node):

        # transfer data from specified node
        # this is a node replacement operation
        #
        self.ntype = node.ntype
        self.mid = node.mid
        self.rchild = node.rchild
        self.lchild = node.lchild
        self.children = node.children

    #
    # end method: TransferData
    
    # method: PrintAttributes
    #
    def PrintAttributes(self):

        # print node attributes
        #
        print("---------------//---------------")
        print("Node Name: " + self.name)
        if self.parent is not None:
            print("Node Parent: " + self.parent.name)
        print("Node index: " + "<{0},{1}>".format(str(self.l), str(self.v)))
        print("Node Type: " + self.ntype)
        if self.mid is not None:
            print("Node id: " + str(self.mid))
        if self.lchild is not None:
            print("Node left child: " + self.lchild.name)
        if self.rchild is not None:
            print("Node right child: " + self.rchild.name)
        print("Private key: " + str(self.key))
        print("Blind key: " + str(self.bKey))
        print("---------------//---------------")

    #
    # end method: PrintAttributes

#
# end class: DataNode

#
# end file: DataNode.py
