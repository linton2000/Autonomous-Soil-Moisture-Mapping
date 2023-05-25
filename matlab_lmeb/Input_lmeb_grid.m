%***********************************************************************
% this routines retrieves soil moisture by inversion of the L-MEB model,
% using a minimization algorithm based on squared difference
% between observed and L-MEB modelled brigthness temperatures
% This is different then the routine Hiresareas_LMEB_simple which optimizes
% using a daily averaged values of Tb and soil moisture and a least squares optimization algorithm
%************************************************************
%
% Xiaoling Wu, adapted to SMAPEx grids
% 05/2013
%
clc;
clear all;
%*****************
% GLOBAL VARIABLES
%*****************
global tbsim
global tbobs
%*****************
% INPUTS
%*****************
%L-MEB parameters 

SMcol = zeros(17568,1);
TBerrcol = zeros(17568,1);

% load brightness temperature data
%cd('/Volumes/Lingling/Working/Bayesian paper/SMAP data download/0510')

load data_0502
load PLMR_TBv_0510_36km    %ELBARA brightness temperature TBv
load PLMR_TBh_0510_36km    %ELBARA brightness temperature TBh
% reshape grid into 1 column
VWCcol = reshape (vwc_pm_new,[],1);
HRcol = reshape (roughness_radio_new,[],1);
tau = veg_opacity_pm_new;
b0 = tau./vwc_pm_new;
bcol = reshape (b0,[],1);
Tbvcol = reshape (PLMR_TBv_0510_36km,[],1);
Tbhcol = reshape (PLMR_TBh_0510_36km,[],1);
Tbvcol(isnan(Tbvcol)) = 0;
Tbhcol(isnan(Tbhcol)) = 0;

% SM retreival
for i=1:4
    
%sand=0.18;   % sand content (0-1)
%clay=0.35;  % clay content (0-1)
%rob=1.3;    % Soil bulk density (g/cm3)
%teta=38;  % Incidence angle (nadir=0)
sand=0.31;   % sand content (0-1)
clay=0.25;  % clay content (0-1)
rob=1.3;    % Soil bulk density (g/cm3)
teta=40;  % Incidence angle (nadir=0

tauh0=bcol(i,1)*VWCcol(i,1);  % Vegetation optical depth at NADIR= b*VWC

tth0=1.;     % Vegetation structure parameter tth
rtt0=1.;     % ttv0= tth0*rtt0;
omgh0=0.0;    % vegetation scattering albedo h-pol
domg0=0.0; % omgv0=omgh0 + domg0;
hsol0=HRcol(i,1);  % Roughness parameter Hr
nsolv0=-1;   % Roughness exponent Nr at v-pol
nsolh0=0;   % Roughness exponent Nr at h-pol
qsol0=0;    % Polarization mixing parameter Qr
b=bcol(i,1);       % Vegetation parameter (Jackson)
ret=0.01;    % initial soil moisture value [v/v]

% Brigthness temperature (Kelvin)
%Tbv=180.5204;  % V-pol 
%Tbh=150.6975;   % H-pol 
Tbv=Tbvcol(i,1);  % V-pol 
Tbh=Tbhcol(i,1);   % H-pol 

% Soil and vegetation Temperatures
% ts1=287;  % Soil temperature at 2-4cm %0905
% ts2=286;  % Soil temperature at 50 cm

% ts1=284;  %0907
% ts2=286;

% ts1=281;  %0910
% ts2=285;

% ts1=285;  %0913
% ts2=285;

% ts1=285;  %0915
% ts2=286;

% ts1=288;  %0918
% ts2=287;
% 
% ts1=286;  %0919
% ts2=288;
% 
% ts1=285;  %0921
% ts2=288;
% 
 ts1=surface_temp_pm_new(i);  %0510
 ts2=surface_temp_pm_new(i);

tc= 300;  % Canopy temperature
tgc0=300;  % Effective ground/canopy temperature --NOT USED

%*****************
% RETRIEVAL
%*****************
% Build input vector
frac_parameters = [sand clay rob ts1 ts2 tc teta tauh0 tgc0 tth0 rtt0 omgh0 domg0 hsol0 qsol0 nsolv0 nsolh0];
Call_lmeb_call(ret);
[x,resnorm,residual,exitflag,output,lambda,jacobian] = Solver_lmeb;
%x
%TBerr(i,1) = resnorm;
SMcol(i,1) = x;
end

SMgrid = reshape(SMcol(1:4),2,2);
SM_PLMR_TB_SMAP_para=SMgrid;
save('SM_PLMR_TB_SMAP_para','SM_PLMR_TB_SMAP_para')
