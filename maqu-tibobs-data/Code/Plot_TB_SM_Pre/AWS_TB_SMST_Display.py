'''
This script is to plot TB, AWS and SMST in time-series.

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

#------------Time settings----------------------------------------
startT = datetime.datetime.strptime("01-10-2016 00:00", "%d-%m-%Y %H:%M")
endT = datetime.datetime.strptime("30-11-2016 23:45", "%d-%m-%Y %H:%M")    # "29-03-2017 14:45"
time_set = '_'+startT.strftime('%m')+startT.strftime('%d')+'_'+endT.strftime('%m')+endT.strftime('%d')+'_'+ endT.strftime('%Y')   # for output
h_freq2 = 900
tmp = (endT-startT).total_seconds()
time_int = int(round(tmp/h_freq2)+1)

#------------read TB ELEBARA dataset----------------------------------------
TB_Name="/home/zhaoh/daspy/PostAna/InSitu_data/Elbara/2016-2018/TB40_2016.dat"
TB_F = open(TB_Name, 'r')
lines = []
header = TB_F.readline()
DATE = []
TBH = []
TBV = []
i=0
TB_T02 = datetime.datetime.strptime("2016-08-07 09:15", "%Y-%m-%d %H:%M") #check the original startT in .dat and the start local time in here. 
tmp2 = (startT-TB_T02).total_seconds()
T_gap = round(tmp2/900)   
print('T_gap for TB is ',T_gap)
time_int2 = time_int
for line in TB_F:
    if i>=T_gap and i < time_int2+T_gap:
        columns = line.split()
        DATE.append(columns[0][0:4]+"-"+ columns[0][5:7]+"-"+columns[0][8:10]+" "+columns[1][0:8])
        TBH.append(numpy.float(columns[3]))
        TBV.append(numpy.float(columns[4]))
    i+=1

print('TB start ',DATE[0], 'TB end ',DATE[-1])
mask = numpy.asarray(numpy.isnan(TBH))  # focus on non TBH under the premise of non TBV correspondingly.
mask_index = numpy.where(mask == True) 

dateList=[]
dateList_mask=[]
for x in range (0, time_int2):
    dateList.append(startT+datetime.timedelta(minutes=15*x))
for i in range(0,len(mask_index[0])):
    dateList_mask.append(dateList[mask_index[0][i]])  #the time in which TBH is without nan.notice --ZH 

df_TBH = pd.DataFrame(numpy.array(TBH),index=dateList)
df_TBV = pd.DataFrame(numpy.array(TBV),index=dateList)

#-------------In situ AWS data------------------------------------------------
pre_loc=os.path.join('/home/zhaoh/daspy/PostAna/InSitu_data/2016SMST/ELBARA-III dataset-2016-2017MeteoData_15min.xlsx')
sheet_name='Data_15mim'
df = pd.read_excel(pre_loc,sheet_name) 
df_t = df['TIMESTAMP']

df1 = df.set_index(pd.DatetimeIndex(df_t))
Tair_insitu = df1[startT:endT]['air temperature at 2m']+273.15
# pre_mask = pre_mask[~mask]
# print type(pre_mask),pre_mask,pre_mask.shape
LDR = df1[startT:endT]['longwave downward']
LUR = df1[startT:endT]['longwave upwelling']
SUR = df1[startT:endT]['shortwave upwelling']
SDR = df1[startT:endT]['shortwave downward']
RH = df1[startT:endT]['relative humidity']
pre_situ = pre_situ1[startT:endT]['Pre_situ_mm']   # 15 min - mm

print('the length for observed precipitation  ', len(LDR))
print('the first selected observed precipitation  ',  LDR)
SB = 5.67 * 10 **(-8)
emis = 0.98   # for grassland
net_L = LUR - (1-emis)*LDR
TG_situ = (net_L/(emis*SB))**(1.0/4)

##---------------AWS output albedo data----
Albedo_situ = SUR/SDR
df_night = df[df['TIMESTAMP'].dt.hour.isin(numpy.array([21,22,23,0,1,2,3,4,5]))]
df_night.set_index('TIMESTAMP',inplace=True)  # must add inplace=True

for i in range(len(df_night.index)):
    for j in range(len(SDR.index)):
        if df_night.index[i] == SDR.index[j]:
            # print df_night.index[i]
            Albedo_situ[j]=0.

for i in range(0,len(Albedo_situ)):
    if Albedo_situ[i] == numpy.inf:
        Albedo_situ[i]=0
    if Albedo_situ[i] > 1:
        Albedo_situ[i]=1.0
    if SUR[i] < 2.8:
        Albedo_situ[i]=0.
        
# out_file=os.path.join('/home/zhaoh/daspy/PostAna/InSitu_data/2016SMST','Albedo_improved.txt')
# f = open(out_file,'w') 
# header=['Datetime','Albedo']
# for j in range(0,len(header)):
    # f.write('%s ' % header[j])
# f.write('\n')    
# for i in range(time_int):
    # f.write('%s	%.2f' % (LDR.index[i],Albedo_situ[i]))
    # f.write('\n')
# f.close() 
        
#-------------In situ SM and SM_eff------
nlayer = 7
InSitu_dir = "/home/zhaoh/daspy/PostAna/InSitu_data/2016SMST"
file_situ=os.path.join(InSitu_dir,'InSitu_SMST_15min_2016.txt')
header1=['Datetime','Time','SM2_5','SM05','SM10','SM20','SM35','SM60','SM100','ST2_5','ST05','ST10','ST20','ST35','ST60','ST100']
dtypes = ['datetime', 'datetime', 'float', 'float']
data_situ = pd.read_csv(file_situ,sep=" ",parse_dates=[['Datetime', 'Time']])
Datetime_Time = data_situ['Datetime_Time']

data_situ1 = data_situ.set_index(pd.DatetimeIndex(Datetime_Time))
A = ['SM2_5','SM05','SM10','SM20','SM35','SM60','SM100','ST2_5','ST05','ST10','ST20','ST35','ST60','ST100']
data_situ2 = data_situ1[startT:endT][A]
SM_situ = numpy.zeros((time_int,nlayer),dtype=numpy.float32)
ST_situ = numpy.zeros((time_int,nlayer),dtype=numpy.float32)
SM_situ[:,0:nlayer] = data_situ2.iloc[:,0:nlayer]
ST_situ[:,0:nlayer] = data_situ2.iloc[:,nlayer:nlayer*2]
print('observed ST_situ ', ST_situ[0:4,:])
print('corresponding time for ST_situ ',data_situ2.index[0:4])

# ------------------------------plot TG, Tair, Tsoil
T_s = 0
T_e =  len(dateList)-1

fig, ax1 = plt.subplots(3,1,figsize=(10,7),dpi=150)

lns1 = ax1[0].plot(dateList[T_s:T_e],numpy.array(SM_situ)[T_s:T_e,0], 'r-',ms=6,label = 'SM_2.5cm')
ax1[0].tick_params(direction='out')
ax1[0].tick_params(top='off',bottom='on',left='on',right='off')
ax1[0].set_ylabel('SM_2.5cm (cm$^3$/cm$^3$)')

ax2 = ax1[0].twinx()
lns2 = ax2.plot(dateList[T_s:T_e],Albedo_situ[T_s:T_e],color = '0.5',linewidth=0.6,label = 'Albedo')
#ax2.plot(dateList_mask[T_s:T_e],RH[~mask][T_s:T_e],color = '0.5',linewidth=0.6)
ax2.set_ylim(ymin = 0)
ax2.set_ylim(ymax = 1.0)
ax2.set_yticks([0,0.25,0.50,0.75,1.0])

labels = [l.get_text() for l in ax2.get_yticklabels()]
labels[0] = '0'
labels[1] = '0.25'
labels[2] = '0.50'
labels[3] = '0.75'
labels[4] = '1.0'
ax2.set_yticklabels(labels)

ax2.invert_yaxis()
ax2.set_ylabel('Albedo') 

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1[0].legend(lns, labs, loc=0,bbox_to_anchor=(0.,1.05,1,.102),ncol=2,mode="expand",borderaxespad = 0.,frameon=False)

ax1[1].plot(dateList[T_s:T_e],TG_situ[T_s:T_e], color='r',linewidth=0.6,linestyle='-',ms=6)
ax1[1].plot(dateList[T_s:T_e],Tair_insitu[T_s:T_e], color ='k',ms=6)
ax1[1].plot(dateList[T_s:T_e],ST_situ[T_s:T_e,0], color='b',linestyle='-',ms=6)
ax1[1].axhline(273.15,color = '#778899',linestyle='--')
ax1[1].legend(['TG','Tair','ST_2.5cm','273.15 K'],prop={'size': 12},loc=0,bbox_to_anchor=(0.,0.96,1,.102),ncol=4,mode="expand",borderaxespad = 0.,frameon=False)
ax1[1].set_ylabel('Temperature (K)')
ax1[1].tick_params(direction='out')
ax1[1].tick_params(top='off',bottom='on',left='on',right='off')


ax1[2].plot(dateList[T_s:T_e],numpy.array(TBH)[T_s:T_e], 'r-',ms=6)
ax1[2].plot(dateList[T_s:T_e],numpy.array(TBV)[T_s:T_e], color='orange',linestyle='-',ms=6)
line, = ax1[2].plot(dateList_mask[T_s:T_e],df_TBH.fillna(method='ffill')[mask][T_s:T_e], marker = 'o', markerfacecolor='white',linestyle='None',markersize = 4, color = 'r')  #  markevery=markers_on
line, = ax1[2].plot(dateList_mask[T_s:T_e],df_TBV.fillna(method='ffill')[mask][T_s:T_e],color='orange', marker = 'o', markerfacecolor='white',linestyle='None',markersize = 4)  # markevery=markers_on

ax1[2].legend(['$T_{B}^{H}$','$T_{B}^{V}$'],prop={'size': 12},loc=0,ncol=2,bbox_to_anchor=(0,0.97,1,.102),mode="expand",borderaxespad = 0.,frameon=False)
ax1[2].set_ylabel("$T_{B}$ (K)",fontsize=12)
ax1[2].tick_params(direction='out')
ax1[2].tick_params(top='off',bottom='on',left='on',right='off')

ax2 = ax1[2].twinx()
ax2.plot(dateList[T_s:T_e],pre_situ[T_s:T_e]*4,color = '0.5')
# ax2.plot(dateList_mask[T_s:T_e],RH[~mask][T_s:T_e],color = '0.5',linewidth=0.6)
ax2.set_ylim(ymin = 0)
ax2.invert_yaxis()

ax2.set_ylabel('Pre (mm/h)') 

# ax1[1].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
# ax1[1].xaxis.set_major_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()
plt.axis('tight')
Out_put="/home/zhaoh/daspy/PostAna/AWS_TB_SMST_plot_2016" +time_set+ ".png"
plt.savefig(Out_put,bbox_inches='tight')
plt.show()
plt.close()    