#project:p2
#submitter:ytian83
#partner: wzhou96

from math import sin, cos, asin, sqrt, pi
from zipfile import ZipFile
from datetime import datetime
import pandas as pd
from graphviz import Graph, Digraph
from IPython.core.display import display, HTML
import matplotlib
from matplotlib import pyplot as plt
from pandas import Series, DataFrame

def backtrace(self, node):
        nodes = []
        while node != None:
            nodes.append(node)
            node = node.back
        return tuple(reversed(nodes))

def Finaledge(time,kk,interval1,ns=True):
    k=mygraph()
    k.node(interval1)
    return edgecon(time,kk,interval1,k,ns=True) 

def edgecon(time,kk,interval1,g,ns=True):
    if time>0:
        if ns==True:
            left=kk[:len(kk)//2]
            left=sorted(left,key=lambda p:p[1])
            right=kk[len(kk)//2:]
            right=sorted(right,key=lambda p:p[1])
            interval2=str(left[len(left)//2][1])
            interval3=str(right[len(right)//2][1])
            ns=False
        else:
            left=kk[:len(kk)//2]
            left=sorted(left)
            right=kk[len(kk)//2:]
            right=sorted(right)
            interval2=str(left[len(left)//2][0])
            interval3=str(right[len(right)//2][0])
            ns=True
        g.edge(interval1,interval2)
        g.edge(interval1,interval3)
        time-=1
        edgecon(time,left,interval2,g,ns)
        edgecon(time,right,interval3,g,ns)
        return g     
def haversine_miles(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = (a/180*pi for a in [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    d = 3956 * c
    return d
class Location:
    capital_lat = 43.074683
    capital_lon = -89.384261
    def __init__(self, latlon=None, xy=None):
        if xy is not None:
            self.x, self.y = xy
        else:
            if latlon is None:
                latlon = (Location.capital_lat, Location.capital_lon)
            self.x = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     Location.capital_lat, latlon[1])
            self.y = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     latlon[0], Location.capital_lon)
            if latlon[1] < Location.capital_lon:
                self.x *= -1
            if latlon[0] < Location.capital_lat:
                self.y *= -1
    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    def __repr__(self):
        return "Location(xy=(%0.2f, %0.2f))" % (self.x, self.y)
    
class BusDay:
    def __init__(self,time):
        self.time=time
        self.service_ids=self.checkid()
        self.root=None 
        self.stops=self.get_stops()
        totalc=[]
        for k in self.stops:
            totalc.append([k.Location.x,k.Location.y]) 
        kk=sorted(totalc)
        interval1=str(kk[len(kk)//2][0]) 
        self.tree= Finaledge(6,sorted(totalc),interval1)  
        self.kk=kk
        self.interval1=interval1
        
    def get_df(self,txt):
        with ZipFile('mmt_gtfs.zip') as zf:
                with zf.open(txt) as f:
                    return pd.read_csv(f)
                
    def checkid(self):
        l=[]
        date=int(self.time.strftime("%Y%m%d"))
        wday=self.time.strftime("%A").lower()
        df = self.get_df("calendar.txt")
        sdf=df[date>df["start_date"]]
        edf=sdf[date<df["end_date"]]
        finaldf=edf[df[wday]==1]
        for i in finaldf["service_id"]:
            l.append(i)
        return sorted(l)
    def get_trips(self,route=None):
        df = self.get_df("trips.txt")
        l=[]
        df=df[df.service_id.isin(self.service_ids)]
        if route!=None:
            df=df[df["route_short_name"]==route]
        df=df.sort_values(by="trip_id")
        for i, j in df.iterrows():
            if j["bikes_allowed"] == 1:
                a=bool(True)
            else:
                a=bool(False)
            trip=Trip(j["trip_id"],j["route_short_name"],a)
            l.append(trip)
        return l   
    def stop_df(self):
        ids=self.service_ids
        trips=self.get_trips()
        l=[]
        for i in trips:
            l.append(i.trip_id)
        stdf=self.get_df("stop_times.txt")
        s1df=stdf[stdf.trip_id.isin(l)]
        stopid=list(s1df.stop_id)
        stopdf=self.get_df("stops.txt")
        s2=stopdf[stopdf.stop_id.isin(stopid)]
        return s2
    def get_stops(self):
        s2=self.stop_df()
        s2=s2.sort_values(by="stop_id")
        final=[]
        for i, j in s2.iterrows():
            stop_id=j.stop_id
            loc = Location(latlon = (j.stop_lat, j.stop_lon))
            
            if j["wheelchair_boarding"] == 1:
                a=bool(True)
            else:
                a=bool(False)
            stop=Stop(j["stop_id"],loc,a)
            final.append(stop)
        return final
    
    def get_stops_rect(self,l1,l2):
        results= self.tree.search(l1,l2,self.kk,self.interval1,self.stops,self.kk)
        return results 
    
    def get_stops_circ(self,xy, r):
        left=xy[0]-r
        right=xy[0]+r
        top=xy[1]+r
        bottom=xy[1]-r
        lr=[left, right]
        bt=[bottom, top]
        circ_area=pi*(r**2)
        square=self.get_stops_rect(lr,bt)
        final=[]
        for i in square:
            x=abs(i.Location.x-xy[0])
            y=abs(i.Location.y-xy[1])
            dis=sqrt(x**2+y**2)
            if dis<r:
                final.append(i)
        return final
    def plot_df(self):
        stoplist=self.get_stops()
        temp=[]
        for i in stoplist:
            stops={}
            stops["stop_id"]=i.stop_id
            stops["xloc"]=i.Location.x
            stops["yloc"]=i.Location.y
            stops["wb"]=i.wheelchair_boarding
            temp.append(stops)
        gh=pd.DataFrame(temp)
        return gh
    def scatter_stops(self, ax):
        df=self.plot_df()
        tdf=df[df.wb]
        fdf=df[df.wb==False]
        ax=ax
        ax=tdf.plot.scatter(x="xloc",y="yloc",ax=ax,color="red",zorder=0)
        ax=fdf.plot.scatter(x="xloc",y="yloc",ax=ax,color="0.7",zorder=1)
        return ax
    def draw_tree(self,ax,ns=True):
        stops=self.get_stops()
        totalc=[]
        for k in stops:
            totalc.append([k.Location.x,k.Location.y]) 
        kk=sorted(totalc)
        interval1=str(kk[len(kk)//2][0])
        k = Finaledge(6,sorted(totalc),interval1) 
        time=7
        root=k.nodes[interval1]
        return self.points(root,ax)
    
    def points(self,root,ax,lw=7,time=7,xlim=(-8,8),ylim=(-8,8)):
        if root.children==[]:
            return 
        if time%2==1:
            time-=1
            x1=float(root.name)
            x2=float(root.name)
            y1=ylim[0]
            y2=ylim[1]
            ax.plot((x1,x2), (y1,y2), lw=time, color="purple")
            self.points(root.children[1],ax,lw,time,xlim=(float(root.name),xlim[1]),ylim=ylim)
            self.points(root.children[0],ax,lw,time,xlim=(xlim[0],float(root.name)),ylim=ylim)
        else:
            time-=1
            x1=xlim[0]
            x2=xlim[1]
            y1=float(root.name)
            y2=float(root.name)
            ax.plot((x1,x2), (y1,y2), lw=time, color="purple")
            self.points(root.children[0],ax,lw,time,xlim=xlim,ylim=(ylim[0], float(root.name)))
            self.points(root.children[1],ax,lw,time,xlim=xlim,ylim=(float(root.name),ylim[1]))
            
class Trip:
    def __init__(self,trip_id,route_id,bikes_allowed):
        self.trip_id=int(trip_id)
        self.route_id=int(route_id)
        self.bikes_allowed=bool(bikes_allowed)
    def __repr__(self):
        return "Trip({}, {}, {})".format(self.trip_id, self.route_id,self.bikes_allowed)
        
class Stop:
    def __init__(self,stop_id,Location,wheelchair_boarding):
        self.stop_id=stop_id
        self.Location=Location
        self.wheelchair_boarding=wheelchair_boarding
        
    def __repr__(self):
        return "Stop({}, {}, {})".format(self.stop_id, self.Location,self.wheelchair_boarding)   
def get_ax():
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return ax
class mygraph:
    def __init__(self):
        self.nodes = {}
    
    def node(self, name):
        self.nodes[name] = Node(self, name)
    
    def edge(self, src, dst):
        for name in [src, dst]:
            if not name in self.nodes:
                self.node(name)
        self.nodes[src].children.append(self.nodes[dst])
        
    def find(self, src, dst):
        self.visited = set()
        return self.nodes[src].find(dst)
    
    def search(self,l1,l2,search,interval1,stops,research,first=True):
        limit_we=[] 
        limit_ns=[]
        limit_we.append(l1[0])
        limit_we.append(l1[1])
        limit_ns.append(l2[0])
        limit_ns.append(l2[1]) 
        l1=[]
        m=self.nodes[interval1]
        return self.finding(m.search(limit_we,limit_ns,l1),m.name,research,limit_we,limit_ns,stops)     
    def finding(self,allnodes,root,searching,l1,l2,stops,ns=True):
        total=[]
        groups=[]
        for k in allnodes:
            groups.append(self.find(root,k))
        return self.final_work(l1,l2,groups,searching,total,stops)
    
    def final_work(self,l1,l2,groups,searching,total,stops,d=0,ns=True):  
        if d==len(groups):
            pass
        else:
            n=0
            search1=searching
            nodes=groups[d]
            d+=1
            while n<7:
                if ns==True:
                    search1=sorted(search1)
                    ns=False
                    adding=[]
                    for k in search1:
                        if k[0]==float(nodes[n].name):
                            adding.append(k)     
                    if n==6:
                        m=float(nodes[n].name)
                        if l1[0]<=m and l1[1]<=m:
                            search1=search1[:search1.index(adding[0])]
                            search1.extend(adding)
                        elif l1[0]<=m and l1[1]>=m:
                            None
                        else:
                            search1=search1[search1.index(adding[0]):]  

                    else: 
                        if str(nodes[n].children[0].name)==nodes[n+1].name:
                            search1=search1[:search1.index(adding[0])]
                            search1.extend(adding)
                        else:
                            search1=search1[search1.index(adding[0]):] 

                else:
                    search1=sorted(search1,key=lambda p:p[1])
                    
                    adding=[]
                    ns=True
                    for k in search1:
                        if k[1]==float(nodes[n].name):
                            adding.append(k)         
                    if str(nodes[n].children[0].name)==nodes[n+1].name:
                        search1=search1[:search1.index(adding[0])]
                        search1.extend(adding)
                    else:
                        search1=search1[search1.index(adding[0]):] 
                n=n+1
            total.extend(search1)
            self.final_work(l1,l2,groups,searching,total,stops,d) 
        return self.checking(l1,l2,total,stops)
    def checking(self,l1,l2,total,stops):
        final=[]
        points=[]
        for k in total:
            if k[0]>=l1[0] and k[0]<=l1[1]:
                if k[1]>=l2[0] and k[1]<=l2[1]:
                    points.append(k)          
        for k in points: 
            for n in stops:
                if n.Location.x==k[0] and n.Location.y==k[1]:
                    final.append(n)
                        
        m= list(set(final))
        return m
                
class Node:
    def __init__(self, graph, name):
        self.graph = graph
        self.name = name
        self.children = []
        #self.left=self.children[0]
        #self.right=self.children[1]
        
    def __repr__(self):
        return "node %s" % self.name

    def find(self, dst):
        todo = [self]
        self.back = None
        self.graph.visited.add(self.name)

        while len(todo) > 0:
            curr = todo.pop(0) 

            if curr.name == dst:
                return backtrace(self, curr)
            else:
                for child in curr.children:
                    if not child.name in self.graph.visited:
                        todo.append(child) 
                        child.back = curr
                        self.graph.visited.add(child.name)

                        
        return None
    def search(self,we,ns,leaves,tt=True):
        if tt==True:
            tt=False
            if self.children!=[]:
                if float(self.name)>=we[0] and float(self.name)>=we[1]:
                    self.children[0].search(we,ns,leaves,tt)
                elif we[0]<=float(self.name) and float(self.name)<=we[1]:
                    self.children[0].search(we,ns,leaves,tt)
                    self.children[1].search(we,ns,leaves,tt,)
                else:
                    self.children[1].search(we,ns,leaves,tt)

            else:
                leaves.append(self.name)

        else:
            tt=True
            if self.children!=[]:
                if float(self.name)>=ns[0] and float(self.name)>=ns[1]:
                    self.children[0].search(we,ns,leaves,tt)
                elif ns[0]<=float(self.name) and float(self.name)<=ns[1]:
                    self.children[0].search(we,ns,leaves,tt)
                    self.children[1].search(we,ns,leaves,tt)
                else:
                    self.children[1].search(we,ns,leaves,tt)

            else:
                leaves.append(self.name)
        return leaves