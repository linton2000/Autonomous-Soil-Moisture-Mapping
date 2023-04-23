'''
This script is to check time information for time-series data

Copyright: Hong Zhao, ITC, University of Twente
Date: 11-03-2020
E-mail: h.zhao@utwente.nl
'''

import xlrd, os
import datetime
import matplotlib.pyplot as plt
import numpy,string
import pandas as pd
from numpy import nan


startT = datetime.datetime.strptime("12-08-2018 15:15", "%d-%m-%Y %H:%M")
endT = datetime.datetime.strptime("28-08-2019 15:45", "%d-%m-%Y %H:%M")
time_set = "_2018_2019"   # for output
h_freq2 = 900
tmp = (endT-startT).total_seconds()
time_int = int(round(tmp/h_freq2)+1)

#-------------In situ AWS data------
pre_loc = os.path.join('/home/zhaoh/daspy/PostAna/InSitu_data/2018SMST/AWS_2018_2019.xlsx')
sheet_name='Data_timeCheck'
df = pd.read_excel(pre_loc,sheet_name) 
df_t = df['TIMESTAMP']
df1 = df_t.dt.strftime('%Y-%m-%d %H:%M')
print(df1[0])


# date_rng = pd.date_range(start='2017-03-29 13:30', end='2018-08-27 21:00', freq='15min')  # date format consistent with former one
date_rng = pd.date_range(start='2018-08-12 15:15', end='2019-08-28 15:45', freq='15min')
for i in range(len(df1.index)):  # check the data
    t1 = str(df1[i])[0:16]    # t1 = 
    t2 = str(date_rng[i])[0:16]
    print(t1,t2)
    if t1==t2:
        continue
    else:
        print(i)
        break
