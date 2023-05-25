function [out]=Hoperator_calc(mc,day,grid)
global optopt fractions parameters ind scale
global sand clay rob BULK CLAY MalvernClay MalvernSand
global woodland bares LANDCOVER30m

% Load optical depth
TAU1031=evalin('base','OUTPUT1031.OPTICALDEPTH');
TAU1107=evalin('base','OUTPUT1107.OPTICALDEPTH');
TAU1121=evalin('base','OUTPUT1121.OPTICALDEPTH');
%------------------
% Options
%------------------
%scale=40     % SMOS type footprint scale retrieval
scale=1;       % PLMR 1km scale retrieval or AMSRE-E type retrieval
woodland=4;  % to model openwoodland as grassland
bares=4;  % to model bare soil as grassland
teta=38.5;  %Incidence angle
%woodland=2    % to model open woodland as forest 
optopt=0;   %parameter for Lmeb_call not to treat Tau as variable


%--------------------
% load Ancillary data
%---------------------
load LANDCOVER
load TEMPERATURES
load TEXTURE
% get temperature data for specific date
eval(['Ts1=Daily_temperatures.data{3}(Daily_temperatures.data{1}==',char(day),');']); % surface soil temperature (K) at about 2-5cm
eval(['Ts2=Daily_temperatures.data{2}(Daily_temperatures.data{1}==',char(day),');']);  % soil temperature at depth (K) at about 50 cm;  ts1 & ts2 are used 
eval(['Tc=Daily_temperatures.data{4}(Daily_temperatures.data{1}==',char(day),');']);    % to compute effective soil Tg using xa & xb  

%---------------------------
%radiative transfer parameters 
%---------------------------

% bare soil
frac_parameters(:,1)=[1.3 1.13 0 Ts1 Ts2 Tc teta NaN 300 1 1 0 0.05 0.5 0 0 1]'; 

% grassland
frac_parameters(:,2)=[1.3 1.13 0 Ts1 Ts2 Tc teta NaN 300 1 1 0 0.05 0.5 0 0 1]';  

%  crops
frac_parameters(:,3)=[1.6 1.1 0 Ts1 Ts2 Tc teta NaN 300 1 8 0 0 0.2 0 -1 0]';  

% Forest
frac_parameters(:,4)=[0 0 0 Ts1 Ts2 Tc teta NaN 300 0.46 1 0.07 0 0.12 0 0 0]'; 


%-------------------------------
% pixel by pixel jacobian
% ------------------------------
k=1;
[long,lat] = pixcenters(grid.refmat,size(TAU1031));
for j=5:46
     for i=6:42
      % get VEGETATION OPTICAL DEPTH 
      % if NaN, go to next pixel (No Jacobian calculated)
      eval(['Tau=TAU',day,'(i,j);']);
      if isnan(Tau)
           out(1,k)=NaN;
           out(2,k)=NaN;
           k=k+1;
          continue
      else
      
      % VEG TYPE FRACTIONS
      [fractions,fflag,cloud]=getfrac(lat(i),long(j),grid.refmat(1,2));   %to become a 4 element vector "fractions
      
     %  Determine domimant class 
      ind=find(fractions==max(fractions));
      a=size(ind);
      if a(2)>1  % MIXED PIXELS (more then one dominant class)
          ind=max(ind);   % model the vegetation type with higher code !!!TO BE RE-CONSIDERED
          mixed=1;
      end
          
      % SOILTYPE
              [sand,clay,rob]=getsoil(lat(i),long(j),grid.refmat(1,2));  
  
        % Calculate Jacobian for specific pixel and write output
        %***********************************************
        parameters=frac_parameters(:,ind);
        parameters(8)=Tau;
        [J]=Jacobian_LMEB(mc);
        out(1,k)=J(1);
        out(2,k)=J(2);
        k=k+1;
       clear J
       end 
     end  %end column loop 
 end  % end row loop
       clear Tc Ts1 Ts2 frac_parameters
       clear b data lat long scale teta woodland 
       clear Tau_bare Tau_crop Tau_forest Tau_grass i j
       clear optopt yobs fractions frac_parameters ind scale
       clear sand clay rob CLAY MalvernClay MalvernSand

