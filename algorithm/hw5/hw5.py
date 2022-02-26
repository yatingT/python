#!/usr/bin/env python
# coding: utf-8

# In[4]:


n = int(input())
l=[]
for i in range(int(n)):
    current=input()
    l.append(int(current))


# In[5]:


l


# In[6]:


def hw5(l, n, total):
    if n%2==1:
        return False
    half =([[False for i in range(total + 1)] for i in range(n + 1)])
    for i in range(n + 1):
        half[i][0] = True
    for i in range(1, total + 1):
         half[0][i]= False
    for i in range(1, n + 1):
        for j in range(1, total + 1):
            if j<l[i-1]:
                half[i][j] = half[i-1][j]
            if j>= l[i-1]:
                half[i][j] = (half[i-1][j] or half[i - 1][j-l[i-1]])
    return half[n][total]
         
total = int(sum(l)/2)
n = len(l)
if hw5(l,n,total)==True:
    print("T")
if hw5(l,n,total)==False:
    print("F")

