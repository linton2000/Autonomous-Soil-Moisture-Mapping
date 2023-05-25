function [ymod,autres,temperature]=tauw1i(para,jqm,aide)
autres=0;

% L-MEB model
% function used for inversion by invnp.m (JPW 03/2003-2007)
% CARE (modif % tauw1.m):
%   -tbsky is computed here (it is not an input); Tair is derived from Tgc  !
%    MODIFIED BY ROCCO , 10/09/2007: Tair is derived from Tsurface
%   - input = teta1 & teta2 (teta is computed here)
%   - input = rapomg (omgv=omgh*rapomg is not an input);
%   - output tb= [tbV(teta1), tbH(teta2)]
%   - initialization of autres


%%%%function y=tauw1(freq, teta, xmv, tauh, tc, t2, cpol, omgv, omgh , rob, sand, clay, xa, xb, hsol, qsol, nsol, tbsky, ifwat, twat, sal)
%%%%% modele tau-omega % version itt /05/2001: identique a tauw93.f
%%%%% VERSION 1: 06/2001 : includes water surfaces (ifwat test) and reflect.m subroutine
%%%%% launched by subroutine tauw93mN.m (N=version)

%#ok<*GVMIS>
global conf;
%%%% PARA
xmv = abs(para(1));
tau0 = abs(para(2));     %tau at nadir
tgc = para(3);
tth = para(4);
rtt = para(5);
omgh = para(6);
domg = para(7);
hsol = para(8);
qsol = para(9);
nsolv = para(10);
nsolh = para(11);

%%%% AIDE
freq = aide(1);
tc = aide(2); %eff veg temp
ts1 = aide(3); %ground temp at surface
ts2 = aide(4); %ground temp at depth
rob = aide(5);
sand = aide(6);
clay = aide(7);
xa = aide(8);
xb = aide(9);
ifwat = aide(10);
twat = aide(11);
sal = aide(12);
ifmodit = aide(13);
teta1 = aide(14);
teta2 = aide(15);

% specific to inversion
if ifmodit==1
    % inversion mode: all temperatures are eqaul to Tgc (effective ground-canopy temperature)
    tc= tgc;
    ts1 = tgc;
    ts2 = tgc;
end

omgv = omgh + domg;

rd = 180/pi;
lo = 0.3/freq;
f = freq*1e9; % frequency in Hz
eps0 = 1.+ 0.i; %air dielectric constant


% **** compute TETA - % specific to inversion
teta1 = sort(teta1);
teta2 = sort(teta2);
tetax = [teta1, teta2];	% vecteur ligne
lig = angone(tetax);
teta = sort(tetax(lig));

xmu = cos(teta/rd);
xnu = sin(teta/rd);

ttv =  tth*rtt;

xpolh = xmu.*xmu+tth*xnu.*xnu;
xpolv = xmu.*xmu+ttv*xnu.*xnu;

tauv = tau0*xpolv;
tauh = tau0*xpolh;

gamv = exp(-tauv./xmu);
gamh = exp(-tauh./xmu);


%%% TBSKY CALIBRATION

% %%% computing TBSKY % specific to inversion
%   ouput : tsky (=total (sky + atmosphere) downwelling radiation at surface level
%	zz	Altitude of the surface (derived from the surface pressure field)	km
%	T2m	Surface (screen level) air temperature	K
%	Q2m	Surface (screen level) air specific humidity	g kg-1  (vary between 0 to 25; dry ~ 5)
%	RR	Rain rate	mm h-1
%  zz=0; t2m=tgc; q2m=10; rr=0;
zz = 0; t2m = ts1; q2m = 10; rr = 0;   % MODIFIED FROM ORIGINAL
tbsky = skytl(teta, zz, t2m, q2m, rr);
% tbsky=0;
%tbsky=[tbsky0, tbsky0];
%disp(['tbsky=', num2str(tbsky)]);

%%%% DISPLAY SURFACE PARAMS:
if conf(1) == 1
   disp('----------------------------------------')
   disp('    ifr,       tau5h,       tgc')
   %disp([ifr, tau5h, tgc]);
   disp([0, 0, tgc]);
   disp('tauv,     tauh,       gamv,       gamh');
   disp([tauv(1),tauh(1),gamv(1),gamh(1)]);
   disp('    xmv,       omgv,       omgh,       cpol,     hsol,    qsol');
   %disp([xmv,omgv, omgh, cpol, hsol, qsol]);
   disp([xmv,omgv, omgh, 0, hsol, qsol]);
end

%%%% TB CALCULATION
if ifwat==1
   % ifwat=1: Surface =WATER
   teff=twat;
   hsol=0;
   qsol=0;
   nsolv=0;
   nsolh=0;
   
   if (teff<=272.65)
      % WATER = PURE ICE (eps-ice ~= 3.15 + i*1e-3 at freq ~ L-band))
      eps2=eps_ice(freq,teff); % pure ice (without impurities), ref: HUT formulation (J. Pulliainen)
      disp('PURE ICE')
   else
      % saline water permittivity
      eps2=dobeaus(freq,teff, sal); %% saline water
      disp('FRESH WATER')
   end
   
else
   % else: Surface = SOIL
   
   % compute tg (if xb=0, tg=ts1) (ifmodit==1, tg=ts1=ts2=tgc)
   tg=ts2+((xmv/xa).^xb).*(ts1-ts2);
   %disp(['tg=', num2str(tg)]);
   
   if ifmodit==0
      % direct mode: tgc is not retrieved
      % it is roughly estimated here from tc, ts1 and ts2 for information only,
      % to check the inversion process
      bt=1.7;
      at= bt*(1. -exp(tau0));
      if (at>= 1) 
         at=1; end
      if (at<= 0) 
         at=0; end
      tgc= at* tc + (1.-at) * tg;
      para(3) = tgc; % !!! only if tgc is not retrieved ...
   end
   
   
   % *** soil permittivity
   % !!! types of routine depends on frequency (dobsol ou wang)
   %eps2=3-2i;
   teff=tg;
   if freq<=18
      eps2=dobsol(f,teff,xmv,sand,clay,rob);
   else
      eps2=wang(f,teff,0.17,0.13,sand,clay,rob,xmv);
   end
   
end

%disp(['eps2=', num2str(eps2)])


% ***************** Surface Reflectivity
yy= reflect (teta, eps0, eps2, hsol, qsol, nsolv, nsolh);

rv20r=yy(1,:);
rh20r=yy(2,:);
tbsv=(1-rv20r).*tg;
tbsh=(1-rh20r).*tg;
%[tbsv', tbsh']

% **** TAU-OMEGA model GLOBAL: Vegetation + soil
xv=(1-omgv).*(1-gamv).*(1+rv20r.*gamv)*tc;
xh=(1-omgh).*(1-gamh).*(1+rh20r.*gamh)*tc;

tbv=xv+(tbsv+tbsky.*rv20r.*gamv).*gamv;
tbh=xh+(tbsh+tbsky.*rh20r.*gamh).*gamh;

if conf(2) == 1
   % **********************************
   % **********************************
   % *** PLOT
   
   plot(teta,tbv,'+',teta,tbv,'-',teta,tbh,'o',teta,tbh,'--')
   xlabel('INCIDENCE ANGLE (�C)')
   ylabel('BRIGHTNESS TEMPERATURE (K)')
   normtxt
   
   text(0.05,0.11,['FREQ=',freq,'GHz', '  WS=', num2str(xmv)])%, '  VWC=', num2str(wc)])
   %text(0.05,0.05,['EPS2=',num2str(eps2)])
   fic= 'tauw93g';
   %pr(fic);
   
end		%flplt


% --- compute tb for teta1 & teta2 % specific to inversion
if isempty(teta1)
   tbv=[];
else
   lig1=compfilt(teta, teta1);
   tbv=tbv(lig1);
end
if isempty(teta2)
   tbh=[];
else
   lig2=compfilt(teta, teta2);
   tbh=tbh(lig2);
end


% --- OUTPUT= TB ---
ymod=[tbv, tbh]; %% specific to inversion
temperature=[tg,tgc];