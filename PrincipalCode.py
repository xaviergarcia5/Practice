# Xavier 
# 6/23 - 6/27 -2022
import numpy as np


def Mo_from_mag(Mw):
    '''
    param (Mw) float, moment magnitude of Earth
    return value is a float in dyne-cm
    '''
    expo = 1.5 * (Mw + 10.7)
    Mo = 10 ** expo
    return Mo

def Mw_from_Mo(Mo):
    M = 0.66667 * np.log10(Mo)
    Mw = M - 10.7
    return Mw

def read_mgfunction(filename):
    '''
    input filename, data type: str, 
    returns a list of floats 
    '''
    print("Reading file" + filename); #to know what is inside
    mglist = []#empty list
    with open(filename,'r') as data_file:
        data_file.readline()#to avoid the first line
        for line in data_file: 
            if len(line.split()) < 13 :
                continue;
            else:
                data = line.split()[4]
                mag = float(data)
                mglist.append(mag) #mag is a float
    print("Reading Catalog of Lenght" , len(mglist))
    return mglist
'''
mglist = read_mgfunction("../Data/socal_earthq.txt")
print (mglist)
TotalCounter = 0 #
for magnitude in mglist:
    TotalCounter = Mo_from_mag(magnitude) + TotalCounter
print("Total Moment" , TotalCounter , "dyne-cm")

Mw = Mw_from_Mo(TotalCounter)
print("Equivalent Moment Magnitude" , Mw)

learthquake = np.max(mglist)

mearthquake = np.min(mglist)

print ("largest Earthquake" , learthquake , "Minimunm Earthquake" , mearthquake)
'''
   
#Mo = Mo_from_mag(Mw)
#print(Mo)

#Mw = Mw_from_Mo(Mo
#print(Mw)




'''
import matplotlib as plt
lat = []
lon = []
withfile = open('socal_earth.txt', 'r')
#data = file.read() line.split()
#print(data)
'''

'''
lat = []
lon = []



import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt

df = open('socal_earth.txt', 'r')
geometry = [Point(xy) for xy in zip(df['LON'], df['LAT'])]
gdf = GeoDataFrame(df, geometry=geometry)   

#this is a simple map that goes with geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15);

'''

'''
import matplotlib.pyplot as plt
import numpy as np

with open('socal_earth.txt', 'r') as f: 
    lines = f.readlines()
    x = [float(line.split()[0]) for line in lines]
    y = [float(line.split()[1]) for line in lines]
plt.plot(x ,y)
plt.show()

'''

'''
filename = "../Data/socal_earth.txt"
latlist = []#empty list
with open(filename,'r') as data_file:
    data_file.readline()#to avoid the first line
    for line in data_file: 
        if len(line.split()) < 13 : #normal lines have 12 columns(in this case)
            continue;
        else:
            data = line.split()[6] 
            lat = float(data)
            latlist.append(lat) #lat is a float
    print("Reading Catalog of Lenght" , len(latlist))
print(latlist)

#I think I would have to make two lists (one of lat (y) and one of long (x)). Then plot on the map x and y.

'''

def read_position_arrays(filename):

    '''
    Reads the X, Y, and Z positions of the earthquakes
    :param filename: string, name of text file from Caltech SCSN.
    :returns: lon, array of floats.  lat, array of floats.  depths, array of floats. 
    '''
    lonlist, latlist, depthlist = [], [], []
    print(filename)
    with open(filename, 'r') as f:
        f.readline();  # skip header line
        for line in f:
            if len(line.split()) < 13:   # if "fake" line
                continue;
            else:  # if "real data" line
                latlist.append(float(line.split()[6])) # "append" adds a single item to the existing list. It doesn't return a new list of items but will modify the original list by adding the item to the end of the list
                lonlist.append(float(line.split()[7]))#method that returns a floating-point number for a provided number or string
                depthlist.append(float(line.split()[4]))#The split() method splits a string into a list.
    return lonlist, latlist, depthlist;


def write_position_arrays(lons, lats, depth, filename):
    ofile = open(filename, 'w'); #w is writing permission for the opened file
    for i in range(len(lons)): #The range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number.
        ofile.write("%.5f %.5f %.2f \n" % (lons[i], lats[i], depth[i]) );# %f formatter is used to input float values, or numbers with values after the decimal place. (.5decimal places )
    ofile.close();
    print(filename)
    return;#Functions often interact with each other through returned values. This is crucial because when a function finishes executing, the values it created or stored “die”. Therefore those values are local


import matplotlib.pyplot as plt
import numpy as np

x, y, depth = read_position_arrays("../Data/socal_earth.txt");
write_position_arrays(x, y, depth, "dummy_file.txt"); #3 colum file


plt.figure()
plt.plot(x, y, '.', color = 'red') 
plt.xlabel('Longitude', fontdict = font1)
plt.ylabel('Latitude', fontdict = font1)
plt.title('Southern California Earthquakes (June 2021)', fontdict = font1)
plt.xlim(-123, -110)
plt.ylim(30, 38)
plt.savefig("examplemap.png")

