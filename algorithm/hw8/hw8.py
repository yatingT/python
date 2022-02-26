#!/usr/bin/env python
# coding: utf-8

# In[1]:


input_size = input()
input_size=input_size.split()
r = int(input_size[0]); c = int(input_size[1]); size = r + c + 2
m = [[0 for i in range(size)] for j in range(size)]
for i in range(1, r+1):
    m[0][i] = 1
    m[size-1-i][size-1] = 1
    temp=input()
    for j in range(c):
        t=temp.split()
        m[i][j+r+1]=int(t[j])


# In[5]:


from collections import defaultdict
class Graph:
    def __init__(self, graph):
        self.graph = graph  
        self.row = len(graph)
    def bfs(self,node,t,pa):
        meet = [False]*(self.row)
        q = []
        q.append(node)
        meet[node] = True
        while q:
            p = q.pop(0)
            for i, value in enumerate(self.graph[p]):
                if meet[i] == False and value > 0:
                    q.append(i)
                    meet[i] = True
                    pa[i] = p
        return True if meet[t] else False

    def ff(self, source, sink):
        p = [-1]*(self.row)
        flow = 0 
        while self.bfs(source, sink, p) :
            pf = float("Inf")
            s = sink
            while(s !=  source):
                pf = min(pf, self.graph[p[s]][s])
                s = p[s]
            flow +=pf
            v = sink
            while(v !=  source):
                u = p[v]
                self.graph[u][v] -= pf
                self.graph[v][u] += pf
                v = p[v]
        return flow
 

g = Graph(m) 
source = 0; 
sink = r+ c + 1
print (g.ff(source, sink))
 


# In[ ]:




