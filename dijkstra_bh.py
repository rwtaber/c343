from sys import maxint

class NoParentE     : pass
class NoLeftChildE  : pass
class NoRightChildE : pass

class Item :
    def __init__ (self, name, value=None) :
        self.name = name
        self.value = value
        self.position = None
        self.previous = None
    def __repr__ (self) :
        return self.name + " : " + str(self.value)

class Path :
    def __init__ (self, node) :
        self.nodes = [node]
        self.len = 0
    def append (self, node, distance) :
        self.nodes.append(node)
        self.len += distance

class BinaryHeap :
    def __init__ (self,fromList=None) :
        self.elems = [None]
        self.size = 0
        if fromList :
            self.size = len(fromList)
            self.elems.extend(fromList[:])
            for i in range(self.size/2,0,-1) :
                self.moveDown(i)

    def isEmpty (self) : return self.size == 0

    def getSize (self) : return self.size

    def findMin (self) : return self.elems[1]

    def getParentIndex (self,i) :
        if i == 1 :
            raise NoParentE
        else :
            return i/2

    def getLeftChildIndex (self,i) :
        if i*2 > self.size :
            raise NoLeftChildE
        else :
            return i*2

    def getRightChildIndex (self,i) :
        if i*2+1 > self.size :
            raise NoRightChildE
        else :
            return i*2+1

    def swap (self,i,j) :
        ip = self.elems[i].position
        jp = self.elems[j].position
        temp = self.elems[i]
        self.elems[i] = self.elems[j]
        self.elems[j] = temp
        self.elems[i].position = ip
        self.elems[j].position = jp

    def moveUp (self,i) :
        try :
            p = self.getParentIndex(i)
            if self.elems[i].value < self.elems[p].value :
                self.swap(i,p)
                self.moveUp(p)
        except NoParentE :
            pass

    def insert (self,k) :
        self.elems.append(k)
        self.size += 1
        self.elems[self.size].position = self.size
        self.moveUp(self.size)

    def updateKey(self,i,v) :
        self.elems[i].value = v
        self.moveUp(i)

    def minChildIndex (self,i) :
        try :
            lc = self.getLeftChildIndex(i)
            rc = self.getRightChildIndex(i)
            if self.elems[lc].value < self.elems[rc].value :
                return lc
            else :
                return rc
        except NoRightChildE :
            return lc

    def moveDown (self,i) :
        try :
            c = self.minChildIndex(i)
            if self.elems[i].value > self.elems[c].value :
                self.swap(i,c)
                self.moveDown(c)
        except NoLeftChildE :
            pass

    def delMin (self) :
        self.elems[1] = self.elems[self.size]
        self.elems[1].position = 1
        self.size -= 1
        self.elems.pop()
        self.moveDown(1)

    def extractMin (self) :
        temp = self.elems[1]
        self.delMin()
        return temp

    def __repr__ (self) :
        return repr(self.elems[1:])

class Graph:
    def __init__ (self, nodes, neighbors, weights) :
        self.nodes = nodes
        self.neighbors = neighbors
        self.weights = weights
        self.q = [None]

    def setSource(self,s) :
        for x in range(0, len(self.nodes)) :
            if self.nodes[x] == s :
                self.nodes[x].value = 0
            else :
                self.nodes[x].value = maxint
            self.nodes[x].position = x + 1
        self.q = BinaryHeap(fromList=self.nodes)

    def relax(self,u,v) :
        if v.value > u.value + self.weights[(u, v)] :
            v.previous = u
            self.q.updateKey(v.position, u.value + self.weights[(u, v)])

    def compute_shortest_paths(self,s) :
        self.setSource(s)
        for i in range(1, self.q.getSize()) :
            a = self.q.extractMin()
            for j in self.neighbors[a] :
                self.relax(a, j)

    def build_shortest_path(self,u) :
        ret = Path(u)
        t = u
        while t.previous != None :
            ret.append(t.previous, self.weights[t.previous, t])
            t = t.previous
        return ret
