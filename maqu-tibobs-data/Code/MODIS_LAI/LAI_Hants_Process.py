'''
This script is to to smooth (filter) MODIS LAI data using HANTS algorithm

Copyright: Hong Zhao, ITC, University of Twente
Date: 11-03-2020
E-mail: h.zhao@utwente.nl
'''


import sys
import os
import string
import numpy
import datetime
from HANTS import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import scipy
import scipy.signal

#---------lai T from modis
LAI_modisF=os.path.join('/home/zhaoh/daspy/PostAna/ObsModel','modis_2019_lai.asc')
lai = open(LAI_modisF,'r')
T_lai_modis=[]
lai_time = []
for line in lai:
    lai_modis=str.split(line)
    tmp2 = lai_modis[0]
    lai_time.append( datetime.datetime.strptime(tmp2,"%Y-%m-%d"))
    T_lai_modis.append(numpy.float(lai_modis[2])) #from MODIS    
lai.close()
print(lai_time)

#--------------Run HANTS for a single point------
time_int = len(lai_time)
ni = time_int
nb = time_int  
ts = range(ni)
nf = 10   # change this value
 
low = 0.1
high = 6.2
HiLo = 'Lo'
fet = 0.05
delta = 0.1
dod = 1
fill_val = -9999.0

y = pd.np.array(T_lai_modis)
y[~pd.np.isfinite(y)] = fill_val

[hants_values, outliers] = HANTS(ni, nb, nf, y, ts, HiLo, low, high, fet, dod, delta,fill_val)
# print hants_values
Input='LAI_2019_HANTS.txt'
InputF = open(Input,'w')
InputF.write('%s\n' % 'TIME	original_value	hants_value')
for i in range(time_int):
    InputF.write('%s	' % lai_time[i])
    InputF.write('%.2f	' % T_lai_modis[i])    
    InputF.write('%.2f\n' % hants_values[i])
InputF.close()

LAI_hants = pd.Series(hants_values,index=lai_time)
print(lai_time)
upsampled = LAI_hants.resample('D')  # can change for an expected frequency
print(upsampled)
LAI_hants_interpolated = upsampled.interpolate(method='linear')

startT = datetime.datetime.strptime('2017-01-01 00:00',"%Y-%m-%d %H:%M")
endT = datetime.datetime.strptime('2020-01-01 00:00',"%Y-%m-%d %H:%M")

LAI_hants_sel = LAI_hants_interpolated[startT:endT]
print(LAI_hants_sel)


Input='LAI_sel_2019_15min.txt'
InputF = open(Input,'w')
InputF.write('%s\n' % 'TIME	LAI_hants')
for i in range(len(LAI_hants_sel.index)):
    InputF.write('%s	' % LAI_hants_sel.index[i])
    InputF.write('%.2f\n' % LAI_hants_sel.values[i])    
InputF.close()

print('finish calculating')

#-------------------plot -----------
fig, ax = plt.subplots(1,1,figsize=(10,7),dpi=150)
plt.plot(lai_time[:], hants_values[:], 'r-', label='HANTS')
plt.plot(lai_time[:], T_lai_modis[:], 'b.', label='Original data')
#plt.plot(lai_time[:], y_sav[:], 'g-', label='SAV')
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('MODIS LAI (m$^2$/m$^2$)')
plt.gcf().autofmt_xdate()
plt.axis('tight')
Out_put="/home/zhaoh/daspy/PostAna/Plot_Com6/NDVI_HANTS_2019.png"
plt.savefig(Out_put,bbox_inches='tight')
plt.show()
plt.close()  

#-------------------plot -----------
# fig, ax = plt.subplots(1,1,figsize=(10,7),dpi=150)
# plt.plot(LAI_hants_sel.index, LAI_hants_sel, 'r-', label='LAI')

# plt.legend(loc=0)
# plt.xlabel('Date')
# plt.ylabel('MODIS LAI (m$^2$/m$^2$)')
# plt.gcf().autofmt_xdate()
# plt.axis('tight')
# Out_put="/home/zhaoh/daspy/PostAna/Plot_Com6/NDVI_HANTS_201915min.png"
# plt.savefig(Out_put,bbox_inches='tight')
# plt.show()
# plt.close()  

                   
