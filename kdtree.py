import numpy as np
import math

class KDNode(object):
    def __init__(self,featIndex,val,parent=None):
        self.featureIndex=featIndex
        self.val=val
        self.left=None
        self.right=None
        self.parent=parent
    
    def __str__(self):
        return "featurIndex={0},val={1}".format(self.featureIndex,self.val)

class KDTree(object):
    def __init__(self,data,labels):
        self.data=np.array(data)
        self.labels=np.array(labels)
        self.root=self.build(self.data,None)
        
    def choose_split_feature(self,data):
        m,n=data.shape
        maxVar=-math.inf
        featIndex=-1
        for i in range(n):
            varI=np.var(data[:,i])
            # print(varI)
            if(varI>maxVar):
                maxVar=varI
                featIndex=i
        return featIndex

    def getMedianIndex(self,data,featureIndex):
        orders=np.argsort(data[:,featureIndex])
        t=len(data)//2
        return data[orders],t
        # return np.median(data[:][featureIndex])
    
    def build(self,data,root):
        if(len(data)==0):
            return None
        featIndex=self.choose_split_feature(data)
        newData,idx=self.getMedianIndex(data,featIndex)
        leftData=newData[:idx]
        rightData=newData[idx+1:]
        # print(leftData,rightData,featIndex,newData[idx,:])
        node=KDNode(featIndex,newData[idx,:],root)
        node.left=self.build(leftData,node)
        node.right=self.build(rightData,node)
        return node

    def print(self,root):
        queue=[]
        if(root==None):
            return
        # print(root.val,root.featureIndex)
        # self.print(root.left)
        # self.print(root.right)
        queue.append(root)
        while(len(queue)>0):
            node=queue.pop(0)
            print(node)
            if(node.left!=None):
                queue.append(node.left)
            if(node.right!=None):
                queue.append(node.right)
        
    def search(self,testdata):
        minDis=math.inf
        def distance(node,testdata):
            return np.linalg.norm(node.val-testdata)
        def to_plan_distance(node,testdata):
            return np.abs(node.val[node.featureIndex]-testdata[node.featureIndex])

        def tunnel(node,testdata):
            tmpNode=None
            queue=[]
            queue.append(node)
            while(len(queue)>0):
                tmpNode=queue.pop(0)
                if(testdata[tmpNode.featureIndex]<=tmpNode.val[tmpNode.featureIndex]):
                    if(tmpNode.left!=None):
                        queue.append(tmpNode.left)
                else:
                    if(tmpNode.right!=None):
                        queue.append(tmpNode.right)
            return tmpNode
            
        result=[]
        targetNode=None
        result.append(tunnel(self.root,testdata))
        while(len(result)>0):
            node=result.pop()
            while(True):
                tmpDis=distance(node,testdata)
                if(minDis>tmpDis):
                    minDis=tmpDis
                    targetNode=node
                if(node.parent!=None):
                    parentNode=node.parent
                    planeDis=to_plan_distance(parentNode,testdata)
                    if(tmpDis>planeDis):
                        sibleNode=parentNode.right if node==parentNode.left else parentNode.left
                        result.append(tunnel(sibleNode,testdata))
                    node=node.parent
                else:
                    break
        # print(targetNode.featureIndex,targetNode.val)
        return targetNode
            



data=[[3,1,4],[2,3,7],[4,3,4],[2,1,3],[2,4,5],[6,1,4],[1,4,4],[0,5,7],[5,2,5],[4,0,6],[7,1,6]]
labels=[1,2,3,2,3,2,2,1,1,2,1]
tree=KDTree(data,labels)
tree.print(tree.root)
# tree.search([3,4,9])



