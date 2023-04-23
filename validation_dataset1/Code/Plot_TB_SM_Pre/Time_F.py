import datetime
from astral import *
def round_time(dt=None, round_to=60):
   if dt == None: 
       dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   rounding = (seconds+round_to/2) // round_to * round_to
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
   

   
def TB_Time_Shift(dateT):
    a = Astral()
    location = a['Beijing']
    timezone = location.timezone
    # print 'Timezone: ', timezone
    # print 'lat and lon ',location.latitude, location.longitude

    MQ = Location()
    MQ.name = 'Maqu'
    MQ.region = 'region'
    MQ.latitud = 33.9178
    MQ.longitude = 102.1574
    MQ.timezone = 'Asia/Harbin'
    MQ.elevation = 3647  # unit: m

    sun_BJ = location.sun(local=True,date=dateT,use_elevation=True)
    sun_Maqu = MQ.sun(local=True,date=dateT,use_elevation=True)
    noon_BJ = str(sun_BJ['noon'])[0:19]
    noon_Maqu = str(MQ.solar_noon(dateT,local=True))[0:19]
    time_shift = datetime.datetime.strptime(noon_Maqu,"%Y-%m-%d %H:%M:%S")\
               -datetime.datetime.strptime(noon_BJ,"%Y-%m-%d %H:%M:%S")\
               +datetime.timedelta(hours=8)  
    return time_shift     # time_shift.total_seconds()