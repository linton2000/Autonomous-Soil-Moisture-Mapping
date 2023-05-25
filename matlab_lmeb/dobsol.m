function epsol=dobsol(fr,tsol,xmv,sand,clay,rob)

% calcul de la permitt du sol (Dobson, 1995)
% !!!: salsol=param du calcul
% tsol en K
% fr en Hz !!!!!

% **************************************
% **** INIT

permit=8.854e-12;

alp=0.65;
ros=2.66;
epwi=4.9;

%!!!
salsol=0.65;
ts=tsol-273.15;


if (ts <= -0.5)
%     SOIL = FROZEN SOIL  (Ulaby et al., 1986, p2101)     
epx=5.;
epy=-0.5;
epsol=epx+i*epy + 0 *xmv;
       
else



if (xmv<0.02) & (sand >=0.9)

% DRY SAND (ref Matzler, 1998)
epsi=2.53;
epss=2.79;
xa=0.002;
f0=0.27e9;

epsol=epsi+(epss-epsi)./(1-i*(fr/f0)) +i*xa;
   
else

% **************************************
% **** SALINE WATER
%  ref: saline water (Ulaby/M/F p2024)

       xa=1+1.613e-5*ts*salsol-3.656e-3*salsol...
      +3.21e-5*salsol*salsol-4.232e-7*(salsol^3);
       epw0=xa*(87.134-1.949e-1*ts-1.276e-2*ts*ts+2.491e-4*(ts^3));
       xb=1+2.282e-5*ts*salsol-7.638e-4*salsol ...
      -7.76e-6*salsol*salsol+1.105e-8*(salsol^3);
       topi=xb*(1.1109e-10-3.824e-12*ts+6.938e-14*ts*ts ...
      -5.096e-16*(ts^3));

       seff=-1.645+1.939*rob-2.256*sand+1.594*clay;
       cx=(epw0-epwi)./(1.+i*topi*fr);
       epfw=epwi+cx-i*seff*(ros-rob)./(2*pi*fr*permit*ros*xmv);

       bet1=1.275-0.519*sand-0.152*clay;
       bet2=1.338-0.603*sand-0.166*clay;
       eps=(1.01+0.44*ros)^2-0.062;
       
       x=1+rob*(eps^alp-1)/ros+(xmv.^bet1).*(real(epfw).^alp)-xmv;
       y=(xmv.^bet2).*(abs(imag(epfw)).^alp);
       epx=x.^(1/alp);
       epy=y.^(1/alp);
       epsol=epx-i*epy;

 end	% frozen soil
 end	% dry sand
 



