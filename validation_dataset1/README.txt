Version of readme: 14-March-2020
The detail is given in Su et al.(2020), "Multiyear in-situ L-band microwave radiometry of land surface processes on the Tibetan Plateau" 
DOI:

Corresponding author(s): Bob Su (z.su@utwente.nl), Jun Wen (jwen@cuit.edu.cn), 
                     Yijian Zeng (y.zeng@utwente.nl) Hong Zhao (h.zhao@utwente.nl)

##############################Data############################################################################
ELBARA-III dataset-2016-2017.csv contains eight sheets
- MeteoData_15min_20160101_0315:     contains air temperature, precipitation amount,four components radiation measurement (i.e., up- and down-welling shortwave and longwave radiations). 
- MeteoData_30min_20160101_0315:     contains air temperature, precipitation amount,four components radiation measurement (i.e., up- and down-welling shortwave and longwave radiations). 
- SMST_LC:       contains soil moisture and soil temperature measured at different depths
- SMST_Z:        contains soil moisture and soil temperature measured at different depths
- ELBARA-III TB: contains ELABRA-III measured brightness temperature TB at different incidence angle for H and V polarizations. 
- SMAP TB:       contains SMAP L1C brightness temperature TB over Maqu ELABRA-III site. 
- MODIS LAI_HANTS:     contains processed MODIS LAI using HANTS algorithm. 
- Field_Unit:    contains the description and unit for each field in each sheet.

##############################Data###########################################################################
ELBARA-III dataset-2017-2018.csv contains seven sheets
- MeteoData_30min:     contains air temperature, precipitation amount,four components radiation measurement (i.e., up- and down-welling shortwave and longwave radiations). 
- SMST_LC:       contains soil moisture and soil temperature measured at different depths
- ELBARA-III TB: contains ELABRA-III measured brightness temperature TB at different incidence angle for H and V polarizations. 
- SMAP TB:       contains SMAP L1C brightness temperature TB over Maqu ELBARA-III site.
- MODID LAI_HANTS:     contains processed MODIS LAI using HANTS algorithm. 
- LAI_IN SITU:   Contains the data measured by LAI-2000. 
- Field_Unit:    contains the description and unit for each field in each sheet.

##############################Data###########################################################################
ELBARA-III dataset-2018-2019.csv contains six sheets
- MeteoData_30min:     contains air temperature, precipitation amount,four components radiation measurement (i.e., up- and down-welling shortwave and longwave radiations). 
- SMST_LC:       contains soil moisture and soil temperature measured at different depths
- ELBARA-III TB: contains ELABRA-III measured brightness temperature TB at different incidence angle for H and V polarizations.. 
- SMAP TB:       contains SMAP L1C brightness temperature TB over Maqu ELBARA-III site.
- MODIS LAI_HANTS:     contains processed MODIS LAI using HANTS algorithm. 
- Field_Unit:    contains the description and unit for each field in each sheet.

##############################Data#########################################################################
FluxDataAllField.csv contains four sheets
- 2016_2017:   contains the data measured by Integrated Eddy Covariance system (EC150 analyzer, CSAT3A anemometer, HMP155A relative humidity and temperature, and
109-L air temperature) (Campbell scientific, USA) 
- 2017_2018:   contains the data measured by Integrated Eddy Covariance system (EC150 analyzer, CSAT3A anemometer, HMP155A relative humidity and temperature, and
109-L air temperature) (Campbell scientific, USA)
- 2018_2019:   contains the data measured by Integrated Eddy Covariance system (EC150 analyzer, CSAT3A anemometer, HMP155A relative humidity and temperature, and
109-L air temperature) (Campbell scientific, USA)
- Field_Unit:   contains the description and unit for each field in each sheet. Also see eddycovariance_rawdata_metafile.pdf
## please note the fluxes such as H, LE, CO2, u* can be extracted from these sheets. We provide all data for all possible usages. 
   
#################################Data########################################################################
ELBARA-III dataset-2016-2019MODIS_LAI_8daily.csv
- Contain 8-daily raw data extracted from MCD15A2H - MODIS/Terra+Aqua Leaf Area Index (500 m resolution)
  The data can be downloaded at https://lpdaac.usgs.gov/products/mcd15a2hv006/.
  The download process can be seen from 'MODIS_Download_Procedure.pdf' 
  LAI processed by HANTS written by python: https://github.com/gespinoza/hants

#################################SMAP footprint at Maqu site######################
"SMAP L1C over Maqu ELBARA site.tif" shows the location of SMAP footprint for every snapshot (the resolutions are very low, so the red spot, which is 102.15E 33.90N exactly, covers these locations).  
SMAP L1C product can be downloaded from https://earthdata.nasa.gov/


#################################Code########################################################################
-AWS_Time_Check: AWS_TB_30min_timeCheck.py, check time in series
-MODIS_LAI: MODIS_LAI_Extract.py, LAI_Hants_Process.py, HANTS.py. 
-Plot_TB_SM_Pre: AWS_TB_SMST_Display.py, display figures. 
-SMAP-TB: SMAP L1C TB reading.m

############################################################################################################
  