function [ysim, autres, temperature] = lmeb_call(ret, param)

%#ok<*GVMIS>
global conf;
ifmodit = 0;      % ifmodit=0 = l-meb in direct/forward modeling mode : tc, ts1, ts2 given by aide() are used to compute tb
% if modit=1 =  l-meb is in inversion mode and Tgc is retrieved
freq = 1.41; % Frquency (GHz)

%%%% SOIL TEXTURE
sand = param(1);  % Sand (%)
clay = param(2);   % Clay (%)
rob = param(3);   % bulk soil density (g/cm3)

% Parameters used to compute Tg = effective soil/ground temperature , (Wigneron et al., 2001)
%xa=1; xb=0; %(t-surf= t-down)
xa = 0.3;
xb = 0.3; % to compute tg

% TEMPERATURE (ts1 & ts2 are used to compute effective soil Tg using xa & xb)
ts1=param(4);       % surface soil temperature (K) at about 2-5cm
ts2=param(5);       % soil temperature at depth (K) at about 50 cm;
tc=param(6);        % canopy temperature

%%%% INCIDENCE ANLGE
teta=param(7);
teta1 = teta;
teta2 = teta;


% WATER PARAMETERS:
% WATER: valid if ifwat=1 % twat= water temperature (K); sal= water salinity (o/oo)
ifwat=0; %(ifwat=1 for water surface)
twat=300;
sal=0;

% !!! INIT MODEL PARAM
%if (ij==1) tauh0=0; else tauh0=abs(pend(2)); end %tauh0=0.2;  %
mc=ret(1);   % soil moisture [v/v]
% mc=evalin('base','groundmc'); % ONLY IF running HR_RETRIEVAL!!

%if optopt==0
tauh0=param(8);  % optical depth at NADIR= b*WVC
%elseif optopt==1
%tauh0=ret(2);     % if retrieving optical depth
%end

tgc0=param(9);   % tgc = effective ground/canopy temperature (Cf Wigneron et al., 2007)
tth0=param(10);    % tth= equivalent to cpol at H (Cf Wigneron et al., 2007)
rtt0=param(11);   % ratio ttv = rtt * tth (Cf Wigneron et al., 2007)
omgh0=param(12);
domg0=param(13);  % OMEGA: omgv = omgh + domgvh (Cf Wigneron et al., 2007)

%%%% SOIL ROUGHNESS
qsol0=param(15);
nsolv0=param(16);
nsolh0=param(17);

% hsol0=ret(2); % ONLY IF  running HR_RETRIEVAL!!
if param(1)~=0 && param(2)~=0
    hsol0=param(1)-param(2)*mc;
else
    hsol0=param(14);   % if constant
end

%%%% PARAMETERS (aide is constant & para has retrieval params)
aide = [freq, tc, ts1, ts2, rob, sand, clay, xa, xb, ifwat, twat, sal, ifmodit, teta1, teta2];
para = [mc, tauh0, tgc0, tth0, rtt0, omgh0, domg0, hsol0, qsol0, nsolv0, nsolh0];

%%%% COMPUTE TB (ysim = tb)
jqm=0;
[ysim, autres, temperature] = tauw1i(para, jqm, aide);