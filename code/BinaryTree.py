# file: BinaryTree
#

# description: contains the BinaryTree class
#

# import modules
#
from DataNode import DataNode
from anytree.exporter import DotExporter
from anytree import RenderTree
from anytree import PreOrderIter
import math
import itertools

# class: TreeControl
#

class BinaryTree:

    # constructor
    #
    def __init__(self, size=2, uid = None):

        # define initial data
        #
        self.size = size  # number of members in the group
        self.uid = uid  # unique member ID
        self.nodetrack = 1  # number of nodes generated
        self.nodemax = (2*size)- 1  # maximum number of nodes in a tree with self.size members 
        self.height = math.floor(math.log((self.nodemax-1),2))  # height of the tree
        self.root = DataNode() # root of the tree

        # generate an initial tree
        #
        self.BuildTree()

    #
    # end constructor

    # method: AddNodes
    #
    def AddNodes(self, curr_n):

        # add two nodes to keep the tree full
        #
        nl = '<' + str(curr_n.l+1) + ',' + str(2*curr_n.v) + '>'
        curr_n.lchild = DataNode(name=nl, parent=curr_n, l=curr_n.l+1, v=2*curr_n.v, ntype='inter')
        nr = '<' + str(curr_n.l+1) + ',' + str(2*curr_n.v + 1) + '>'
        curr_n.rchild = DataNode(name=nr, parent=curr_n, l=curr_n.l+1, v=(2*curr_n.v)+1, ntype='inter')

    #
    # end method: AddNodes

    # method: WalkTreeBuild
    #
    def WalkTreeBuild(self, curr_n):

        # walk along the tree and add the appropriate nodes
        #
        if curr_n.rchild is not None and curr_n.lchild is not None:
            self.WalkTreeBuild(curr_n.rchild)
            if self.nodetrack is not self.nodemax:
                self.WalkTreeBuild(curr_n.lchild)
        else:
            self.AddNodes(curr_n)
            self.nodetrack = self.nodetrack + 2  # nodes are added in pairs

    #
    # end method: WalkTreeBuild
    
    # method: PreOrderWalk
    #
    def PreOrderWalk(self):

        # traverse the tree in preorder fashion
        #
        return(PreOrderIter(self.root))

    # method: TypeAssign
    #
    def TypeAssign(self):

        # traverse the tree and assign types to each node
        #
        for node in self.PreOrderWalk():
            if node.lchild is None:
                node.ntype = 'member'

    #
    # end method: TypeAssign

    # method: IDAssign
    #
    def IDAssign(self):

        # member ID list generation
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
        for node in self.PreOrderWalk():
            if node.lchild is None:
                node.mid = idlist[c]
                c = c-1
        
    #
    # end method: IDAssign

    # method: BuildTree
    #
    def BuildTree(self):

        # build the tree
        #
        print("Generating Tree with {0} members ...".format(str(self.size).rjust(2)))
        while self.nodetrack is not self.nodemax:
            self.WalkTreeBuild(self.root)

        # assign types
        #
        self.TypeAssign()

        # assign member ID
        #
        self.IDAssign()

    #
    # end method: BuildTree

    # method: TreeExport
    #
    def TreeExport(self):

        # use graphics module to print tree 
        #
        DotExporter(self.root, nodeattrfunc=lambda n: 'label="%s\n%s"' % (n.name, n.mid)).to_picture("TreeExport.png")

    #
    # end method: TreeExport

    # method: TreePrint
    #
    def TreePrint(self):

        # print the tree via the terminal
        #
        for pre, _, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.ntype, node.mid)
        
    #
    # end method: TreePrint

#
# end class: TreeControl

#
# end file: TreeControl
