#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
from random import *


# In[2]:


def load_data(filepath):
    p=[]
    num=0
    with open(filepath,encoding ="UTF-8") as data:
        reader =csv.DictReader(data)
        for row in reader:
            temp={}
            temp["#"]=int(row["#"])
            temp['Name']=row['Name']
            temp['Type 1']=row['Type 1']
            temp['Type 2']=row['Type 2']
            temp['Total']=int(row['Total'])
            temp['HP']=int(row['HP'])
            temp['Attack']=int(row['Attack'])
            temp['Defense']=int(row['Defense'])
            temp['Sp. Atk']=int(row['Sp. Atk'])
            temp['Sp. Def']=int(row['Sp. Def'])
            temp['Speed']=int(row['Speed'])
            p.append(temp)
            num+=1
            if num==20:
                break
    return p


# In[3]:


def calculate_x_y(stats):
    x=stats['Attack']+stats['Sp. Atk']+stats["Speed"]
    y=stats['Defense']+stats['Sp. Def']+stats["HP"]
    
    return (x,y)
    


# In[4]:


# d=[]
# for i in a:
#     d.append(calculate_x_y(i))
# d


# In[5]:


# def find_min(d):
#     dis=[]
#     for i in d:
#         for j in d:
#             if j<=i:
#                 continue
#             dd=[]
#             dd.append(min(i,j))
#             dd.append(max(i,j))
#             dd.append(((d[i][0]-d[j][0])**2+(d[i][1]-d[j][1])**2)**0.5)
#             dis.append(dd)
#     return min(dis,key=lambda x :x[2])
    

def hac(dataset):
    return 
#     l=[]
#     d={}
#     track={}
#     for i in range(len(dataset)):
#         d[i+1]=dataset[i]
#         track[i+1]=dataset[i]
    
#     while len(track)!=0:
# #         print(track)
# #         print(find_min(d))
#         least=find_min(d)
#         print(least)
    
#         if least[0] in range(1,20) or least[1] in range(1,20):
#             del d[least[0]]
#             del d[least[1]]
#         if least[0] in track or least[1] in track:
#             del track[least[0]]
#             del track[least[1]]
#         d[ int(str(least[0])+str(least[1])) ]=(least[2],least[2])
# #         find_min(d)
            
#     return d
    
# hac(d)
    


# In[6]:


def random_x_y(m):
    l=[]
    for i in range(m):
        l.append((randrange(360),randrange(360)))
    return l
random_x_y(10)


# In[7]:


# def imshow_hac(dataset):
    


# In[ ]:




