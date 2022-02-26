#!/usr/bin/env python
# coding: utf-8

# In[139]:


a=[]
line = input().split()
node=int(line[0])
produce=int(line[1])
edge=int(line[2])
for i in range(edge):
    l=input().split()
    a.append((int(l[0]),int(l[1]),int(l[2])) )


# In[148]:


from collections import defaultdict
 
class Graph():
 
    def __init__(self, node):
        self.node = node  
        self.graph = []  
 
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
 
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
 
    def union(self, parent, r, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if r[xroot] < r[yroot]:
            parent[xroot] = yroot
        elif r[xroot] > r[yroot]:
            parent[yroot] = xroot

        else:
            parent[yroot] = xroot
            r[xroot] += 1

    def mst(self):
        k=produce
        r = []  
        idx = 1
        edge = 1
        self.graph = sorted(self.graph, key=lambda x: x[2])
        parent = []
        rank = []
        for node in range(self.node):
            parent.append(node)
            rank.append(0)
        while edge < self.node - 1:
            u, v, w = self.graph[idx]
            idx+=1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                edge+=1
                r.append([u, v, w])
                self.union(parent, rank, x, y)
        r=sorted(r,key=lambda x:x[2])
        r=r[0:-k+1]
        return r[-1][-1]
        

g = Graph(node+1)
for i in a:
    g.addEdge(i[0],i[1],i[2])

print(g.mst())
 

