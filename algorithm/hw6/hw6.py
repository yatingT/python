#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math 
class Graph:  
    def __init__(self, vertices):  
        self.V = vertices  
        self.graph = []    
    def addEdge(self, u, v, w):  
        self.graph.append([u, v, w])   

    def BellmanFord(self, src,name):  
        track=0
        b=False
#         if len(self.graph)>10:
#             return 1
        dist=dict()
        dist=dict.fromkeys(name,0)
        dist[src] =1
        for u, v, w in self.graph: 
            if dist[u] * w/100 >= dist[v]:  
                    dist[v] = dist[u] * w/100 
            if b==False:
                track+=1
                if v == name[0]:
                    b=True 
        return dist,track


# In[3]:


name=[]
v,e = input().split()
g = Graph(int(v)) 
for i in range(int(e)):
    current=input().split()
    g.addEdge(str(current[0]),str(current[1]),int(current[2]))
    if current[0] not in name:
        name.append(current[0])
    
src=name[0]
d=g.BellmanFord("NYSE",name)
print(math.ceil((1-(100/(d[0][src]*100))**(1/d[1]))*100))

