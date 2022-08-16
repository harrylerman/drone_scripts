# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 12:01:29 2022

@author: harry
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import math
import sys
import getopt

def getparams(argv):
    '''
    Parses the input arguments to get the input logfile and other parameters
    '''
    inputfile = ''
    outputfile = ''
    delim='|'
    isanimated = False
    tlog = False
    ulog = False
    try:
        opts, args = getopt.getopt(argv, "hi:d:a:tu")
    except getopt.GetoptError:
        print('plot_pos_data.py -i <inputfile.csv> -d <delimiter> -a <outputfile.gif for animated plot> -t <if a tlog csv> -u <if a ulog csv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('plot_pos_data.py -i <inputfile.csv> -d <delimiter> -a <outputfile.gif for animated plot> -t <if a tlog csv> -u <if a ulog csv>')
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-d"):
            delim = arg
            if delim == 'tab':
                delim = '\t'
        elif opt in ("-a"):
            outputfile = arg
            isanimated = True   
        elif opt in ("-t"):
            tlog = True
        elif opt in ("-u"):
            ulog = True
    return inputfile, delim, outputfile, isanimated, tlog, ulog

def UpdateProgress(workdone):
    """
    Makes a little progressbar while saving animated .gifs
    """
    if workdone > 0:
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone*100), end="", flush=True)

def LatLonToXY(lat,lon,ref_lat,radius):
    """
    Take a set of lat/lon points and convert to global XY (units are meters)
    """
    x = radius*np.radians(lon)*np.cos(np.radians(ref_lat))
    y = radius*np.radians(lat)
    return x, y

def ReadTlog(file, delim):
    """
    Read in data from a csv-converted tlog
    """
    csvfile = open(file, 'r')
    reader = csv.DictReader(csvfile, delimiter=delim)
    
    radius = 6371000

    xcoord = []
    ycoord = []
    alt = []
    time=[]

    isfirst = True

    for row in reader:
        lat = float(row['GPS_RAW_INT.lat'])
        lon = float(row['GPS_RAW_INT.lon'])
        altitude = float(row['ALTITUDE.altitude_relative'])
        tstamp = float(row['timestamp'])
        if math.isnan(lat) or math.isnan(lon) or math.isnan(altitude) or altitude<-0.7:
            continue
        lat = lat*10**-7
        lon = lon*-1*10**-7
        if isfirst is True:
            ref_lat = lat
            isfirst = False
        x, y = LatLonToXY(lat, lon, ref_lat, radius)
   
        xcoord.append(-1.0*x)
        ycoord.append(y)
        alt.append(altitude)
        time.append(tstamp)

    csvfile.close()

    t0 = time[0]
    x0 = xcoord[0]
    y0 = ycoord[0]
    time = [(i - t0)/60.0 for i in time]
    xcoord = [i - x0 for i in xcoord]
    ycoord = [i - y0 for i in ycoord]

    return time, xcoord, ycoord, alt

def ReadUlog(file, delim):
    """
    Read in data from a csv-converted ulog
    """
    csvfile = open(file, 'r')
    reader = csv.DictReader(csvfile, delimiter=delim)

    xcoord = []
    ycoord = []
    alt = []
    time=[]

    for row in reader:
        
        xcoord.append(float(row['x']))
        ycoord.append(float(row['y']))
        alt.append(float(row['z'])*-1.0)
        time.append(float(row['timestamp']))

    csvfile.close()

    t0 = time[0]
    time = [(i - t0)/60000000.0 for i in time]
    
    return time, xcoord, ycoord, alt

def rotate(angle, npoints, xcoord, ycoord, alt, time, ax):
    """
    Function used for animating plots
    """
    i_from = angle*npoints
    # are we on the last frame?
    if i_from + npoints > len(xcoord) - 1:
        i_to = len(xcoord) - 1
    else:
        i_to = i_from + npoints
    ax.view_init(azim=angle)
    # print(i_to, i_from)
    im=ax.scatter(xcoord[i_from:i_to], ycoord[i_from:i_to], alt[i_from:i_to], c=time[i_from:i_to], cmap='gist_rainbow', s=5)
    im.set_clim(time[0],time[-1])
    # print(angle)
    workdone = angle/359.0
    UpdateProgress(workdone)
    return im

def InitFig(xcoord, ycoord, alt):
    """
    Initialize the plot, either static or animated
    """
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(projection='3d')

    npoints = math.ceil(len(xcoord)/360.0)
    
    ax.set_xlabel('lateral x (North) distance, m')
    ax.set_ylabel('lateral y (East) distance, m')
    ax.set_zlabel('altitude, m')
    ax.set_xlim(min(xcoord), max(xcoord))
    ax.set_ylim(min(ycoord), max(ycoord))
    ax.set_zlim(min(alt), max(alt))
    plt.title('Position Telemetry')
    
    return fig, ax, npoints

def StaticPlot(ax, xcoord, ycoord, alt, time):
    # static plot - use if not animating:
    im=ax.scatter(xcoord, ycoord, alt, c=time, cmap='gist_rainbow', s=5)
    im.set_clim(time[0],time[-1])
    cbar = plt.colorbar(im, shrink = 0.3, fraction = 0.05, orientation='vertical')
    cbar.set_label('time since startup, min')
    plt.show()

def AnimatedPlot(fig, ax, npoints, xcoord, ycoord, alt, time, outputfile):
    #use for animation:
    rot_animation = animation.FuncAnimation(fig, rotate, frames = np.arange(0,360,1), fargs = (npoints, xcoord, ycoord, alt, time, ax), interval=50)
    cbar=plt.colorbar(rotate(0, npoints, xcoord, ycoord, alt, time, ax),shrink = 0.3, fraction = 0.05, orientation='vertical')
    cbar.set_label('time since startup, min')
    rot_animation.save(outputfile, writer=animation.PillowWriter(fps=12), dpi=80)


filepath = 'C:/Users/harry/OneDrive/Documents/McGill stuff/dronescripts/'
inputfile, delim, outputfile, isanimated, tlog, ulog = getparams(sys.argv[1:])
infile = filepath+inputfile
outfile = filepath+outputfile

if tlog is True:
    time, xcoord, ycoord, alt = ReadTlog(infile, delim)
elif ulog is True:
    time, xcoord, ycoord, alt = ReadUlog(infile, delim)

fig, ax, npoints = InitFig(xcoord, ycoord, alt)

if isanimated is True:
    AnimatedPlot(fig, ax, npoints, xcoord, ycoord, alt, time, outputfile)
    
else:
    StaticPlot(ax, xcoord, ycoord, alt, time)  
