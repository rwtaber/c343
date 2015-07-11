import random
from bs4 import BeautifulSoup
import httplib2

class WebMap:
    def __init__(self):
        self.counter = 0
        self.web = {}
        self.crank = {}
        self.http = httplib2.Http(timeout = 3)
        self.http.follow_redirects = False

    def WebCrawler(self, startPage, size, Verbose = False):
        if (size > len(self.web) and not(self.web.has_key(startPage))):
            if Verbose == True:
                print "[" + str(self.counter) + "] " + startPage
                self.counter += 1
            try:
                status, response = self.http.request(startPage)
                links = self.__LinkClean(BeautifulSoup(response).find_all('a'))
            except:
                return None
            self.web[startPage] = links
            for page in links:
                self.WebCrawler(page, size, Verbose)

    def __LinkClean(self, soup):
        clean_links = []
        for i in soup:
            t = i.get('href')
            if isinstance(t, (str, unicode)) and t.startswith("http://"):
                clean_links.append(t.encode('ascii', 'ignore'))
        return clean_links

    def PageRank(self, prob, k):
        self.crank = self.web.fromkeys(self.web, 0)
        current = random.choice(self.web.keys())
        while k > 0 :
            if self.crank.has_key(current):
                self.crank[current] += 1
            else:
                self.crank[current] = 0
            if random.random() * 100 < prob :
                current = random.choice(self.web.keys())
            else :
                if not self.web.has_key(current) or not self.web[current]:
                    current = random.choice(self.web.keys())
                else:
                    neighbors = self.web[current]
                    current = random.choice(neighbors)
            k -=1

    def Top(self, t):
        d = self.crank.items()
        d.sort(key = lambda x : x[1], reverse = True)
        return d[:t]

    def returnWeb(self):
        return self.web

    def returnCrank(self):
        return self.crank
