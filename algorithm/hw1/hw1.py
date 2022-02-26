#!/usr/bin/env python
# coding: utf-8

# In[82]:


n = int(input())
time=[]
for i in range(int(n)):
    current=input()
    time.append(int(current))

def opt(l,n):
    final_max=0
    running_max=0
    for i in range (n):
        running_max+=l[i]
        if running_max<0:
            running_max=0
        elif final_max<running_max:
            final_max=running_max
    return final_max

print(opt(time,n))

