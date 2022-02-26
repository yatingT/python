#!/usr/bin/env python
# coding: utf-8

# In[1]:


n = int(input())
p=[]
q=[]
for i in range(int(n)):
    current=input()
    p.append(int(current))
for i in range(int(n)):
    current=input()
    q.append(int(current))


# In[2]:


def merge(A1,A2):
    A = []
    i, j = 0, 0
    while i < len(A1) or j < len(A2):
        if (i < len(A1) and j < len(A2) and A1[i] < A2[j]) or j == len(A2):
            A.append( A1[i] )
            i += 1
        else:
            A.append( A2[j] )
            j += 1
    return A

def count(l1,l2):
    total = 0
    j = 0
    for i in l1:
        while j < len(l2) and l2[j] < i:
            j += 1
        total += j
    return total

def count_inv(l):
    if len(l) == 1: 
        return 0,l
    mid = len(l) // 2
    c1, A1 = count_inv(l[:mid])
    c2, A2 = count_inv(l[mid:])
    c3 = count(A1, A2)
    A = merge(A1, A2)
    return c1+c2+c3,A


# In[3]:


check=[]
for x in sorted(zip(p,q)):
    check.append(x[1])
print(count_inv(check)[0])

