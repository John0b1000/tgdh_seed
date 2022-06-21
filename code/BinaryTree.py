# file: BinaryTree.py
#

# description: contains the BinaryTree class
#

# import modules
#
from DataNode import DataNode
from anytree.exporter import DotExporter
from anytree import RenderTree
from anytree import search
from anytree import PreOrderIter
import math
import itertools

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

        # build an initial tree and print it
        #
        self.BuildTree()

    #
    # end constructor

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

    # method: BuildTree
    #
    def BuildTree(self):

        # build the tree
        #
        print("Generating Tree with {0} members ...".format(str(self.size).rjust(2)))
        print("I am member {0}".format(str(self.uid).rjust(2)))
        while self.nodetrack is not self.nodemax:
            self.WalkTreeBuild(self.root)

        # set node attributes
        #
        self.TypeAssign()
        self.IDAssign()
        self.FindMe()

    #
    # end method: BuildTree

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
    def TreeRefresh(self):

        # refresh appropriate tree attributes
        #
        self.FindMe()
        self.RecalculateNames()

    # method: JoinEvent
    #
    def JoinEvent(self):

        # prepare the tree
        #
        self.TreePrepEvent()

        # create two new nodes at the insertion node
        #
        inserti_node = self.FindInsertion()
        self.AddNodes(inserti_node)
        sponsor_node = inserti_node.lchild  # the sponsor is always the sibling of the new member
        newmemb_node = inserti_node.rchild

        # assign types and IDs
        #
        sponsor_node.SponsorAssign(mid=inserti_node.mid, join=True) 
        inserti_node.InsertionAssign()
        newmemb_node.NewMembAssign(self.nextmemb)

        # signal that a new member has been added
        #
        self.nextmemb = self.nextmemb+1

        # refresh the tree
        #
        self.TreeRefresh()

    #
    # end method: JoinEvent

    # method: LeaveEvent
    #
    def LeaveEvent(self, eid):

        # prepare the tree
        #
        self.TreePrepEvent()

        # find the member to be erased
        #
        for node in self.GetLeaves():
            if node.mid == eid:

                # assign the sponsor
                #
                sponsor_node = list(self.WalkPreOrder(node.GetSibling()))[-1]
                sponsor_node.SponsorAssign(join=False)
                print(sponsor_node.name)

                # transfer data from the sibling node to the parent
                # the parent node is being replaced
                #
                node.parent.TransferDataRemove(node.GetSibling())

        # refresh the tree
        #
        self.TreeRefresh()

    #
    # end method: LeaveEvent

    # method: CalculateGroupKey
    #
    def CalculateGroupKey(self):

        # this method will traverse from the "me" node and calculate the group key
        #
        pass

    # 
    # end method: CalculateGroupKey

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
        for pre, _, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.ntype, node.mid)
        
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
