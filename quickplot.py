# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 00:22:45 2022

@author: harry
"""

import csv
import matplotlib.pyplot as plt
import sys
import getopt

def getparams(argv):
    '''
    Parses the input arguments to get the input logfile and desired parameters
    to plot.
    '''
    inputfile = ''
    delim = '|'
    params = ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:p:")
    except getopt.GetoptError:
        print('quickplot.py -i <inputfile> -d <delimiter> -p <parameters>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('quickplot.py -i <inputfile> -d <delimiter> -p <parameters>')
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-d"):
            delim = arg
            if delim == 'tab':
                delim = '\t'
        elif opt in ("-p"):
            params = arg.split()
    return inputfile, delim, params

def readlog(file, params, delim):
    '''
    Reads in a csv-converted tlog file (should be converted with mavlogparse script)
    Returns a list of timestamps (in unix epoch time)
    Also returns a list of lists to plot - each individual list corresponds to
    one of the input parameters.
    '''    
    #open the file and use Python's csv module to read it:
    csvfile = open(file, 'r')
    reader = csv.DictReader(csvfile, delimiter=delim)   
    plots = [[] for i in range(len(params))] #initialize a list of empty lists
    time = []
    #read in whatever columns we want according to the column header label:
    for row in reader:
        time.append(float(row['timestamp']))
        for i in range(len(plots)): #iterate over desired plotting parameters
            plots[i].append(float(row[params[i]]))   
    #close the file since we're done reading it:
    csvfile.close()
    return time, plots

def plotlog(time,plots,params):
    '''
    Plots the input parameters in a set of stacked plots.
    '''
    if len(plots)>1: #subplots breaks if trying to subplot 1 single plot
        fig, axs = plt.subplots(len(plots))
        for i in range(len(plots)):
            axs[i].plot(time,plots[i])
            axs[i].set_title(params[i], fontsize=10)
        fig.tight_layout()
        plt.show()
    else:
        plt.plot(time,plots[0])
        plt.title(params[0])
        plt.show()        
    return True

inputfile, delim, params = getparams(sys.argv[1:])
filepath = 'C:/Users/harry/OneDrive/Documents/McGill stuff/dronescripts/'
file = filepath+inputfile
time, plots = readlog(file, params, delim)
plotlog(time,plots,params)