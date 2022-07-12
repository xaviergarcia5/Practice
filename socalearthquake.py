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

mglist = read_mgfunction("../Data/socal_earthq.txt")
#print (mglist)
TotalCounter = 0 #
for magnitude in mglist:
    TotalCounter = Mo_from_mag(magnitude) + TotalCounter
print("Total Moment" , TotalCounter , "dyne-cm")

Mw = Mw_from_Mo(TotalCounter)
print("Equivalent Moment Magnitude" , Mw)

learthquake = np.max(mglist)

mearthquake = np.min(mglist)

print ("largest Earthquake" , learthquake , "Minimunm Earthquake" , mearthquake)

   
#Mo = Mo_from_mag(Mw)
#print(Mo)

#Mw = Mw_from_Mo(Mo
#print(Mw)










  

