'''
This script is to extract original MODIS LAI data in point scale (site_lat,site_lon). 
Note: the commented code is to find the location where the point is located in one MODIS image (2400*2400 grid). 

Copyright: Hong Zhao, ITC, University of Twente
Date: 11-03-2020
E-mail: h.zhao@utwente.nl
'''


from pyhdf.SD import SD, SDC
import numpy, string
from math import sin, cos, sqrt, atan2, radians
import re,os
import datetime
import pandas as pd

# file_name='/home/zhaoh/MODIS/MCD15A/MCD15A2H.A2016313.h26v05.006.2016322093624.hdf' 

# hdf = SD(file_name, SDC.READ)
# print hdf.datasets()

# # Read dataset.
# DATAFIELD_NAME='Lai_500m'
# data3D = hdf.select(DATAFIELD_NAME)
# Lai_500m=data3D.get()/10.0
# dim=Lai_500m.shape
# print Lai_500m.shape  # 2400*2400

# lat_f=open('lat_MCD15A3H.A2016217.h26v05.006.2016239132409.txt','r')  # lat for one MODIS image. 
# lat=[]
# i=0
# for line in lat_f.readlines(): 
    # # line = line.strip()
    # # if not len(line) or line.startswith('#'):
        # # continue      
    # if i>0:
        # tmp=re.findall(r"\d+\.?\d*",line)  #extract number from string
        # if tmp==[]:
            # continue
        # lat.append(numpy.float(tmp[0])) #convert list to string using tmp[0]
    # i+=1
# lat_f.close()
# #print lat


# lon_f=open('lon_MCD15A3H.A2016217.h26v05.006.2016239132409.txt','r')  # lon for one MODIS image.
# lon=[]
# i=0
# for line in lon_f.readlines():     
    # if i>0:
        # tmp=re.findall(r"\d+\.?\d*",line)  #extract number from string
        # if tmp==[]:
            # continue
        # lon.append(numpy.float(tmp[0]))
    # i+=1
# lat_f.close()
# #print lon
# print len(lon),len(lat)

# lat_n=numpy.reshape(numpy.array(lat),(dim[0],dim[0]))
# lon_n=numpy.reshape(numpy.array(lon),(dim[0],dim[0]))

# site_lat=[33.9179];
# site_lon=[102.1571];

# dis=numpy.empty((dim[0],dim[0]))
# for i in range(dim[0]):
    # for j in range(dim[0]):
        # dlat=radians(lat_n[i,j]-site_lat[0])
        # dlon=radians(lon_n[i,j]-site_lon[0])
        # a = sin(dlat / 2)**2 + cos(radians(site_lat[0])) * cos(radians(lat_n[i,j])) * sin(dlon / 2)**2
        # dis[i,j]=2 * atan2(sqrt(a), sqrt(1 - a))
# print dis.min()
# dis_loc=numpy.where(dis==dis.min())

# print lat_n[1459,1145], lon_n[1459,1145]

# print dis_loc[0],type(dis_loc[0]),dis_loc[0][0]
dis_loc=numpy.array([1459,1145])

## find the location close to the site location
# Lai_500m_loc=Lai_500m[dis_loc[0],dis_loc[1]]
# print Lai_500m_loc

dir='/home/zhaoh/MODIS/2019_LAI'
m=0
files=[]
datelist=[]
for dirpath, dirnames, filenames in os.walk(dir):
    for filename in filenames:
        if os.path.splitext(filename)[1]=='.hdf':
                 m=m+1
                 yeardoy=filename[10:17]
                 datelist.append(datetime.datetime.strptime(yeardoy, '%Y%j'))
                 files.append(filename)
                 
print m, files


Lai_500m_loc=numpy.empty(m)   
for i in range(m):
    os.chdir(dir)
    
    hdf = SD(files[i], SDC.READ)
    DATAFIELD_NAME='Lai_500m'
    data3D = hdf.select(DATAFIELD_NAME)
    # print data3D.attributes()  # check attribute
    Lai_500m=data3D.get()/10.0
    Lai_500m_loc[i]=Lai_500m[dis_loc[0],dis_loc[1]]
print Lai_500m_loc, Lai_500m_loc.shape


print datelist
Lai_500m_T=pd.Series(Lai_500m_loc,pd.DatetimeIndex(datelist))
Lai_500m_T0=Lai_500m_T.sort_index()
print Lai_500m_T0.index
# print Lai_500m_T0

#------save lai T from modis
LAI_modisF=os.path.join('/home/zhaoh/daspy/PostAna/ObsModel','modis_2019_lai.asc')
lai = open(LAI_modisF,'w')
for i in range(len(Lai_500m_T0.index)):
    lai.write('%8s	' % Lai_500m_T0.index[i])
    lai.write('%6.3f\n' % Lai_500m_T0.values[i])
    # lai.write('%6.3f\n' % (LAI_modis.values[i]*2))
lai.close()


