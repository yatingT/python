#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import re


# In[2]:



a=[]
d={}
line = input().split()

for i in range(int(line[1])):
    l=input().split()
    a.append( (int(l[0]),int(l[1])) )

for i in a:
    if i[0] not in d:
        d[i[0]]=[i[1]]
    else:
        d[i[0]].append(i[1])
        
    if i[1]not in d:
        d[i[1]]=[i[0]]
    else:
        d[i[1]].append(i[0])
        
adj=d


# In[5]:


v=int(line[0])

class hold:  
    def __init__(self, num):  
        self.num = num
        self.path = [] 
        self.depth=0
        
def six(s):
    current=hold(s)
    current.path.append(s)
    q=[]
    q.append(current)
    r=[]
    while (len(q)!=0):
        current=q.pop()
        for i in adj[current.num]:
            if i not in current.path:
                side=hold(i)
                side.path=side.path+current.path
                side.path.append(i)
                q.append(side)
                side.depth=current.depth+1
                if side.depth==5:
                    if side.num not in r:
                        r.append(side.num)
                if side.depth==6:
                    return r
    return r         


# In[6]:


def combine(r):
    re=[];
    for i in range(len(r)):
        re+=six(r[i])
    return re

def find():
    re=six(1)
    week=0
    check = [False for i in range(v+1)] 
    check[1]=True
    num_find=1
    while num_find != v:
        pop=[]
        week+=1
        for i in re:
            if check[i]==True:
                pop.append(i)
            check[i]=True
            if i==v:
                return week
        set1 = set(re)
        set2 = set(pop)
        re = list(set1 - set2)
        if len(re)==0:
            return -1
        num_find=num_find+len(re)
        re=combine(re)
    return -1
  
print(find())

