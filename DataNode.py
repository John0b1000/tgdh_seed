# file: DataNode.py
#

# description: contains the DataNode class
#

# import modules
#
from anytree import NodeMixin

# class: DataNode
#

class DataNode(NodeMixin):

    # constructor
    #
    def __init__(self, name='<0,0>', parent=None, l=0, v=0, ntype='root', uid=None, rchild=None, lchild=None):

        # define class data
        #
        self.name = name  # index value (used as name attribute for graphic generation)
        self.parent = parent  # parent of the node
        self.l = l  # level index
        self.v = v  # number index
        self.ntype = ntype  # node type: root, inter, member, sponsor
        self.uid = uid  # unique member ID
        self.rchild = rchild  # right child of the node 
        self.lchild = lchild  # left child of the node

    # method: PrintAttributes
    #
    def PrintAttributes(self):

        # print node attributes
        #
        print("Node Name: " + self.name)
        if self.parent is not None:
            print("Node Parent: " + self.parent.name)
        print("Node index: " + "<{0},{1}>".format(str(self.l), str(self.v)))
        print("Node Type: " + self.ntype)
        if self.uid is not None:
            print("Node id: " + self.uid)
        if self.lchild is not None:
            print("Node left child: " + self.lchild.name)
        if self.rchild is not None:
            print("Node righ child: " + self.rchild.name)

    #
    # end method: PrintAttributes

#
# end class: DataNode

#
# end file: DataNode.py
