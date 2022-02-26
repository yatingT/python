#!/usr/bin/env python
# coding: utf-8

# In[114]:


def split(word):
    return [int(char) for char in word]
n=int(input())
leaf=input()
l=split(leaf)


# In[115]:




class Node:
    def __init__(self, value,height,p):
        self.height=height
        self.value=value
        self.p=p
        
for i in range(len(l)) :
    l[i]=Node(l[i],n,1)
    
def s(A):
    if len(A) == 1:return A[0]
    middle = len(A) // 2
    A1 = s(A[:middle])
    A2 = s(A[middle:])
    A = merge(A1, A2)
    return A

def merge(a,b):
    new = Node(0,a.height-1,0)
    if new.height % 2 == 0: # the even number "and" case 
        if (a.value == 0) and (b.value == 0):
            new.value=0
            new.p=((a.p+0)+(0+b.p))/2
        elif (a.value == 0 and b.value == 1):
            new.value=0
            new.p=(a.p+0)/2+(b.p+a.p)/2
        elif (a.value==1 and b.value ==0) : #here changed once 
            new.value=0
            new.p=(a.p+b.p)/2+(b.p+0)/2
        elif a.value == 1 and b.value==1:
            new.value=1
            new.p=((a.p+b.p)+(a.p+b.p))/2
    else: # the odd number "or" case 
        if a.value==0 and b.value ==0:
            new.value=0
            new.p=((a.p+b.p)+(b.p+a.p))/2
        elif (a.value == 0 and b.value == 1):
            new.value=1
            new.p=(a.p+b.p)/2 + (b.p+0)/2
        elif (a.value == 1 and b.value == 0) :
            new.value=1
            new.p=(a.p+0)/2 + (a.p+b.p)/2
        elif a.value == 1 and b.value ==1:
            new.value=1
            new.p=(a.p+b.p)/2
    return new

print(s(l).p)


# In[ ]:




