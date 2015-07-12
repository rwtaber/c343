import sys
import urllib2
from urlparse import urljoin
from bs4 import BeautifulSoup

class NoParentE     : pass
class NoLeftChildE  : pass
class NoRightChildE : pass

def crawl_wiki (url):
    webpage = urllib2.urlopen(url)
    soup = BeautifulSoup(webpage)
    link_a = soup.find_all('a')
    pages = set([])
    for a in link_a:
        if a.has_key('href'):
            ahref = a['href']
            if url != ahref and "/wiki/" in ahref and ":" not in ahref and "//" not in ahref: 
                pages.add(urljoin(url, ahref.split("#")[0]))
    if url in pages:
        pages.remove(url)
    return pages

class Node():
    def __init__(self, page):
        self.page = page
        self.value = 0
        self.adj_list = None

    def makeAdjacency(self):
        self.adj_list = crawl_wiki(self.page)

    def getAdjacency(self):
        if self.adj_list == None:
            self.makeAdjacency()
        return self.adj_list    

    def getPages(self):
        for p in self.adj_list:
            print p

    def __repr__ (self) :
        return self.page + " : " + str(self.value)

    def __eq__(self, other):
        return self.page == other.page

    def __ne__(self, other):
        return self.page != other.page

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

class MaxDict():
    def __init__(self):
        self.dict = {}
        self.max_keys = []

    def sortMax(self):
        self.max_keys.sort(key = lambda x: self.dict[x], reverse = True)

    def add(self, key, value):
        if key not in self.dict:
            self.max_keys.append(key)
        self.dict[key] = value
        self.sortMax()

    def rem(self, key):
        if key in self.dict:
            del self.dict[key]
            self.max_keys.remove(key)

    def getV(self, key):
        return self.dict[key]

    def getMax(self, max):
        return list(self.max_keys[:max])

    def __contains__(self, key):
        return key in self.dict

    def __repr__(self) :
        return str(self.dict) 

class Graph():
    def __init__(self, b_site, cycles):
        self.b_site = b_site
        self.graphed = MaxDict()
        self.ungraphed = MaxDict()
        self.ncycles = cycles
        self.ungraphed.add(b_site, Node(b_site))
        self.sites_in_graph = 0

    def setCycles(self, c):
        if c > self.ncycles:
            self.ncycles = c

    def incGNodeV(self, page, v):
        self.graphed.dict[page].value += v
        self.graphed.sortMax()

    def incUGNodeV(self, page, v):
        self.ungraphed.dict[page].value += v
        self.ungraphed.sortMax()

    def checkCycles(self):
        if self.graphed.dict[self.graphed.getMax(1)[0]].value >= self.ncycles:
            return True
        return False

    def addSet(self, s):
        for page in s:
            if page in self.ungraphed:
                self.incUGNodeV(page, 1)
            else:
                self.ungraphed.add(page, Node(page))
 
    def makeGraph(self):
        current = self.ungraphed.getMax(10)
        print "Graphed " + str(self.graphed)
        print
        print "Ungraphed" + str(current)
        print
        for upage in current:
            if upage in self.graphed:
                self.incGNodeV(upage, self.ungraphed.getV(upage).value)
            else:
                self.addSet(self.ungraphed.dict[upage].getAdjacency())
                self.graphed.add(upage, self.ungraphed.getV(upage))
            self.ungraphed.rem(upage)
            if self.checkCycles():
                return None
        self.makeGraph()

if __name__ == "__main__":
    a = Graph("http://en.wikipedia.org/wiki/Indiana", 5)
    a.makeGraph()
