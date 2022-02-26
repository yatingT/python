#Project: p5
#submitter: ytian83
#partner: none

import zipfile
import sqlite3
import os
import pandas as pd
import re
import numpy as np
import io
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.linear_model import LinearRegression
from matplotlib.animation import FuncAnimation
from IPython.core.display import HTML

def open(name):
    return Connection(name)
    
class Connection:
    def __init__(self, name):
        self.db = sqlite3.connect(name+".db")
        self.zf = zipfile.ZipFile(name+".zip")
    def __enter__(self):
        return self
    def __exit__(self,exc_type, exc_value, traceback):
        self.db.close()
        self.zf.close()
    def data(self):   
        df=pd.read_sql("SELECT * FROM places INNER JOIN images ON places.place_id = images.place_id ", self.db)   
        return df
    def list_images(self):
        sorted_df=self.data().sort_values("image")
        return list(sorted_df["image"])
    def image_year(self, image):
        df=self.data()
        return int(df[df["image"]==image]["year"])
    def image_name(self,image):
        df=self.data()
        return df[df["image"]==image]["name"].item()
    def image_load(self,image):
        with self.zf.open(image) as f:
            buf = io.BytesIO(f.read())
            array = np.load(buf)
            return array
    def lat_regression(self, use_code, ax):
        df=self.data()
        temp=[]
        df=df[df["name"].str.startswith("samp")]
        for row in df["image"]:
            ar=self.image_load(row)
            p=(np.count_nonzero(ar[ar==use_code])/(ar.shape[0]*ar.shape[1]))*100
            temp.append(p)
        df["percent"]=temp
        r = LinearRegression()
        r.fit(df["lat"].values.reshape(-1,1), 
              df["percent"].values.reshape(-1,1))
        point=(float(r.coef_), float(r.intercept_))
        ax.scatter(df["lat"], df["percent"])
        y0=ax.get_xlim()[0]*point[0]+point[1]
        y1=ax.get_xlim()[1]*point[0]+point[1]
        ax.plot(ax.get_xlim(),[y0,y1])
        return point
        
    def year_regression(self,name,codes,ax):
        df=self.data()
        df=df[df["name"]==name]
        temp=[]
        for row in df["image"]:
            ar=self.image_load(row)
            p=(np.count_nonzero(ar[np.isin(ar,codes)])/(ar.shape[0]*ar.shape[1]))*100
            temp.append(p)
        df["percent"]=temp
        r = LinearRegression()
        r.fit(df["year"].values.reshape(-1,1), 
              df["percent"].values.reshape(-1,1))
        point=(float(r.coef_), float(r.intercept_))
        ax.scatter(df["year"], df["percent"])
        y0=ax.get_xlim()[0]*point[0]+point[1]
        y1=ax.get_xlim()[1]*point[0]+point[1]
        ax.plot(ax.get_xlim(),[y0,y1])
        return point 
    def color(self):
        use_cmap = np.zeros(shape=(256,4))
        use_cmap[:,-1] = 1
        uses = np.array([
            [0, 0.00000000000, 0.00000000000, 0.00000000000],
            [11, 0.27843137255, 0.41960784314, 0.62745098039],
            [12, 0.81960784314, 0.86666666667, 0.97647058824],
            [21, 0.86666666667, 0.78823529412, 0.78823529412],
            [22, 0.84705882353, 0.57647058824, 0.50980392157],
            [23, 0.92941176471, 0.00000000000, 0.00000000000],
            [24, 0.66666666667, 0.00000000000, 0.00000000000],
            [31, 0.69803921569, 0.67843137255, 0.63921568628],
            [41, 0.40784313726, 0.66666666667, 0.38823529412],
            [42, 0.10980392157, 0.38823529412, 0.18823529412],
            [43, 0.70980392157, 0.78823529412, 0.55686274510],
            [51, 0.64705882353, 0.54901960784, 0.18823529412],
            [52, 0.80000000000, 0.72941176471, 0.48627450980],
            [71, 0.88627450980, 0.88627450980, 0.75686274510],
            [72, 0.78823529412, 0.78823529412, 0.46666666667],
            [73, 0.60000000000, 0.75686274510, 0.27843137255],
            [74, 0.46666666667, 0.67843137255, 0.57647058824],
            [81, 0.85882352941, 0.84705882353, 0.23921568628],
            [82, 0.66666666667, 0.43921568628, 0.15686274510],
            [90, 0.72941176471, 0.84705882353, 0.91764705882],
            [95, 0.43921568628, 0.63921568628, 0.72941176471],
        ])
        for row in uses:
            use_cmap[int(row[0]),:-1] = row[1:]
        use_cmap = ListedColormap(use_cmap)
        return use_cmap

    def animate(self,name):
        df=self.data()
        df=df[df["name"]==name].sort_values("year")
        fig,ax=plt.subplots(figsize=(8,8))
        def new(i):
            ax.cla()
            ar=self.image_load(df.iloc[i]["image"])
            plt.imshow(ar, cmap=self.color(), vmin=0, vmax=255)
        anim=FuncAnimation( fig, new, interval=1000, frames=len(df["image"]))
        html = anim.to_html5_video()
        #plt.close(fig)
        return html
       
    def close(self):
        self.db.close()
        self.zf.close()
    
    