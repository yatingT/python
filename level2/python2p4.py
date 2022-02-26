#project: p4
#submitter:ytian83
#partner:None

import click
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from io import TextIOWrapper
import csv
import pandas as pd
import re
import socket, struct
from collections import defaultdict
import geopandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.core.display import HTML

@click.command()
@click.argument('zip1')
@click.argument('zip2')
@click.argument('mod', type=click.INT)
def sample(zip1, zip2, mod):
    reader = zip_csv_iter(str(zip1))
    reader_list=list(reader)
    header=reader_list.pop(0)
    simple_list=[]
    with ZipFile(str(zip2), "w") as zf:
        with zf.open(str(zip2[:-4])+".csv", "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for i in range(len(reader_list)):
                    if i % mod==0:
                        writer.writerow(reader_list[i])

def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row

def ip2long(ip):
    temp=re.sub("[a-z]","0",ip)
    packedIP = socket.inet_aton(temp)
    return struct.unpack("!L", packedIP)[0]
                
@click.command()
@click.argument('zip1')
@click.argument('zip2')
def sort(zip1, zip2):
    reader = zip_csv_iter(zip1)
    header = next(reader)
    ip_idx = header.index("ip")
    rows = list(reader)
    ip=lambda row:ip2long(row[ip_idx])
    final=sorted(rows,key=ip)
    with ZipFile(str(zip2), "w") as zf:
        with zf.open(str(zip2[:-4])+".csv", "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in final:
                    writer.writerow(row)

def country_open():
    with ZipFile("IP2LOCATION-LITE-DB1.CSV.ZIP") as zf:
            with zf.open("IP2LOCATION-LITE-DB1.CSV") as f:
                country_csv= csv.reader(TextIOWrapper(f))
                for row in country_csv:
                    yield row
                    
@click.command()
@click.argument('zip1')
@click.argument('zip2')
def country(zip1, zip2): 
    reader = zip_csv_iter(zip1)
    header = next(reader)
    header.append("country")
    rows = list(reader)
    country_l=list(country_open())
    r_idx = 0
    r = [int(country_l[r_idx][0]), int(country_l[r_idx][1])]
    with ZipFile(str(zip2),"w") as zf:
        with zf.open(str(zip2).replace(".zip", ".csv"),"w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in rows:
                    temp=ip2long(row[0])
                    while temp > r[1]:
                        r_idx += 1
                        if r_idx == len(country_l):
                            return 
                        r = [int(country_l[r_idx][0]), int(country_l[r_idx][1])]
                    if r[0] <= temp: 
                        row.append(country_l[r_idx][-1])
                        writer.writerow(row)


def world():
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.set_index("name", drop=False, inplace=True)
    return world[world["continent"] != "Antarctica"]

def plot_hour(zipname, hour=None, ax=None):
    reader = zip_csv_iter(zipname)
    header = next(reader)
    cidx = header.index("country")
    time=header.index("time")
    result = defaultdict(int)
    if hour==None:
        time_dict=defaultdict(int)
        for i in range(24):
            time_dict[i]=defaultdict(int)
        for row in reader:
            h=int(row[time][0:2])
            time_dict[h][row[cidx]] += 1
        for di in time_dict:
            for key, value in time_dict[di].items():
                result[key] += value
    else:
        for row in reader:
            if int(row[time][0:2])==hour:
                result[row[cidx]] += 1
    w = world()
    w["color"] = "0.7"
    for country, count in result.items():
        if not country in w.index:
            continue
        color = "lightsalmon" # >= 1
        if count >= 10:
            color = "tomato"
        if count >= 100:
            color = "red"
        if count >= 1000:
            color = "brown"
        w.at[country, "color"] = color
    ax = w.plot(color=w["color"], legend=True, figsize=(16, 4),ax=ax)
    return ax

@click.command()
@click.argument('zipname')
@click.argument('imgname')
def geo(zipname, imgname):
    ax = plot_hour(zipname)
    ax.figure.savefig(imgname, bbox_inches="tight")  
    
@click.command()
@click.argument('zipname')
@click.argument('imgname')
@click.argument('hour', type=click.INT)
def geohour(zipname, imgname, hour):
    ax = plot_hour(zipname, hour)
    ax.figure.savefig(imgname, bbox_inches="tight")      
    


@click.command()
@click.argument('zipname')
@click.argument('name')
def video(zipname, name):
    fig,ax=plt.subplots()
    def new(i):
        ax.cla()
        img=plot_hour(zipname,i,ax=ax)
        return img  
    anim=FuncAnimation( fig, new, frames=24)
    html = anim.to_html5_video()
    with open(name,"w") as f:
        f.write(html)
        plt.close(fig)
        HTML(html)
        
@click.group()
def commands():
    pass

commands.add_command(sample)
commands.add_command(sort)
commands.add_command(country)
commands.add_command(geo)
commands.add_command(geohour)
commands.add_command(video)

if __name__ == "__main__":
    commands()