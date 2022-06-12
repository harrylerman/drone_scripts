# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 12:01:29 2022

@author: harry
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation


def LatLonToXY(lat,lon,ref_lat,radius):
    """
    Take a set of lat/lon points and convert to global XY (units are meters)
    """
    x = radius*np.radians(lon)*np.cos(np.radians(ref_lat))
    y = radius*np.radians(lat)
    return x, y

def rotate(angle):
    ax.view_init(azim=angle)

filepath = 'C:/Users/harry/OneDrive/Documents/McGill stuff/dronescripts/'
# inputfile='2_June.csv'
# inputfile = '24_May.csv'
# inputfile = '11_Apr_test.csv'
inputfile = 'May11.csv'
file = filepath+inputfile

#24may ref coords:
# ref_lat = 45.5064585
# ref_lon = 73.5800438

#11apr ref coords:
# ref_lat = 45.5056466
# ref_lon = 73.5794050

#2jun ref coords:
# ref_lat = 45.5062950
# ref_lon = 73.5800796

#11may ref coords:
ref_lat = 45.5061078
ref_lon = 73.5803112

radius = 6371000

csvfile = open(file, 'r')
reader = csv.DictReader(csvfile, delimiter='\t')

xcoord = []
ycoord = []
alt = []
time=[]

refx, refy = LatLonToXY(ref_lat, ref_lon, ref_lat, radius)
for row in reader:
    lat = float(row['GPS_RAW_INT.lat'])
    lon = float(row['GPS_RAW_INT.lon'])
    altitude = float(row['ALTITUDE.altitude_relative'])
    tstamp = float(row['timestamp'])
    if math.isnan(lat) or math.isnan(lon) or math.isnan(altitude) or altitude<-0.7:
        continue
    lat = lat*10**-7
    lon = lon*-1*10**-7
    x, y = LatLonToXY(lat, lon, ref_lat, radius)
    x -= refx
    y -= refy
    
    xcoord.append(-1.0*x)
    ycoord.append(y)
    alt.append(altitude)
    time.append(tstamp)

csvfile.close()

t0 = time[0]
time = [(i - t0)/60.0 for i in time]
# x0 = xcoord[0]
# xcoord = [i - x0 for i in xcoord]
# y0 = ycoord[0]
# ycoord = [i - y0 for i in ycoord]
# plt.plot(xcoord, ycoord)
# plt.show()

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(projection='3d')
im = ax.scatter(xcoord, ycoord, alt, c=time, cmap='gist_rainbow', s=5)

#use this to remove axes labels (comment out for static image that uses labels):
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# ax.set_zticklabels([])

#below is for a static image, DONT USE, DEPRECATED, SEE ABOVE:
# im = ax.plot(xcoord, ycoord, alt)

#use this to set axes labels (comment out for rotating image without labels):
ax.set_xlabel('lateral distance, m')
ax.set_ylabel('lateral distance, m')
ax.set_zlabel('altitude, m')

#colorbar info
cbar = plt.colorbar(im, shrink = 0.3, fraction = 0.05, orientation='vertical')
cbar.set_label('time since startup, min')
plt.title('May 11 mission-mode position telemetry')

#to kill all axis markings:
# plt.grid(None)
# plt.axis('off')

# static plot - use if not animating:
plt.show()

#use for animation:
# rot_animation = animation.FuncAnimation(fig, rotate, frames = np.arange(0,362,2), interval=50)
# rot_animation.save(filepath+'rotation11May.gif', writer=animation.PillowWriter(fps=24), dpi=80)