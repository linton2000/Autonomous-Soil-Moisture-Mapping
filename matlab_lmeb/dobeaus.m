function epeau=dobeaus(freq,t2, sal)

% JPW // ITT 06/2001
% ref: saline water / pure water (Ulaby/M/F p2020 / 2024)

% t2 en K (vecteur ou var)
% freq en GHz, fr en Hz, 
% sal= water salinity (°/oo) (sea~ 32.5)
% **************************************
% **** INIT

permit=8.854e-12;
epwi=4.9;
%!!!
t=t2-273.15;
fr=freq*1.e9;

%  ref: saline water (Ulaby/M/F p2024)
  a=1.0+1.613e-5*t*sal-3.656e-3*sal + 3.21e-5*(sal^2)-4.232e-7*(sal^3);
  epw0=a*(87.134-1.949e-1*t-1.276e-2*t*t+2.491e-4*(t^3));
  b=1.+2.282e-5*t*sal-7.638e-4*sal -7.76e-6*(sal^2)+1.105e-8*(sal^3);
  topi=b*(1.1109e-10-3.824e-12*t+6.938e-14*t*t -5.096e-16*(t^3));
       
io25=sal*(0.18252-1.4619e-3*sal+2.093e-5*(sal^2) -1.282e-7* (sal^3));
dt=25-t;       
phi=dt*(2.033e-2 + 1.266e-4*dt+ 2.464e-6*dt*dt - sal *(1.849e-5-2.551e-7*dt + 2.551e-8*dt*dt));       
ionic=io25*exp(-phi)

%epor=epwi + (epw0-epwi)/(1+ (topi*fr)^2)
%epoi=  (topi*fr*(epw0-epwi))/(1+ (topi*fr)^2)+ ionic/(2*pi*permit*fr)

epeau=epwi+(epw0-epwi)./(1.0+i*topi*fr)- i*ionic/(2*pi*permit*fr);
