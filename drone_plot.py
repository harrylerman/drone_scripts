fr# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:36:30 2022

@author: harry
"""
import numpy as np

def LatLonToXY(lat,lon,ref_lat,radius):
    """
    Take a set of lat/lon points and convert to global XY (units are meters)
    """
    x = radius*np.radians(lon)*np.cos(np.radians(ref_lat))
    y = radius*np.radians(lat)
    return x, y

def InterpDronePos(tstamp, drone_times, drone_data):
    """
    Interpolates the drone's position at the input timestamp
    Assumes drone timestamps are monotonically increasing   
    """
    #get the index of the drone data that is closest in time to the receiver /
    #data (lower bounded tstamp)
    dtstamp_i = drone_times[drone_times <= tstamp].argmax()
    
    #drone data points to interpolate, the input tstamp is between these points
    drone_data1 = drone_data[dtstamp_i]
    drone_data2 = drone_data[dtstamp_i+1]
    
    #times, lats, lons of each drone data point    
    dt1 = drone_data1[0]
    dlat1 = drone_data1[1][0]
    dlon1 = drone_data[1][1]
    
    dt2 = drone_data2[0]
    dlat2 = drone_data2[1][0]
    dlon2 = drone_data2[1][1]
    
    #points to interpolate    
    xi = [dt1, dt2]
    lati = [dlat1, dlat2]
    loni = [dlon1, dlon2]
    
    #interpolate for latitude
    interp_lat = np.interp(tstamp, xi, lati)
    
    #interpolate for longitude
    interp_lon = np.interp(tstamp, xi, loni)
    
    return interp_lat, interp_lon

#set up some empty lists to plot
x = []
y = []
i = []

#read in times and intensities here for receiver
rec_data = []
# should be something like a list of [time, intensity]

#read in times and positions here for drone
drone_data = []
#should be something like a list of [time, (lat, lon)]

drone_times = drone_data[:,0]

#reference point x,y position
ref_lat = #receiver lat
ref_lon = #receiver lon
radius = 6371000 #earth radius in meters
x0, y0 = LatLonToXY(ref_lat, ref_lon, ref_lat, radius)

#iterate over antenna data
for dat in rec_data:
    #receiver timestamp and intensity
    rtstamp = dat[0]
    intensity = dat[1]
    
    #get the interpolated drone position at the receiver tstamp time
    ilat, ilon = InterpDronePos(rtstamp, drone_times, done_data)
    
    #convert the interpolated drone position to local x,y coords
    xglobal, yglobal = LatLonToXY(ilat,ilon,ref_lat,radius)
    xlocal = xglobal - x0
    ylocal = yglobal - y0
    
    #append the x,y position and intensity to some lists we can plot
    x.append(xlocal)
    y.append(ylocal)
    i.append(intensity)

#scatterplot of x, y, i

    
    