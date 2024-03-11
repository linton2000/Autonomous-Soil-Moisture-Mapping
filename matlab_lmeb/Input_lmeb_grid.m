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
% Linton Charles, modified file for Tib-Obs dataset
% 05/2023

clear;
%#ok<*GVMIS>
global tbsim; %#ok<NUSED>
global tbobs; %#ok<NUSED>

% Load Tib-Obs Maqu network Data
% [Tbvcol, Tbhcol, stemp, dtemp, lai, true_sm] = load_tibetan(nrecs);

% Load Oval Area sampling data
R1 = getfield(load("geodata_r1.mat"), 'fdata');
R2 = getfield(load("geodata_r2.mat"), 'fdata');
R3 = getfield(load("geodata_r3.mat"), 'fdata');
R_all = vertcat(R1, R2, R3);
Tbhcol = mean(R_all(:, 2:5), 2, "omitnan");
Tbvcol = mean(R_all(:, 6:9), 2, "omitnan");
Tbvcol = Tbvcol(~isnan(Tbvcol));
Tbhcol = Tbhcol(~isnan(Tbhcol));

% Initialise result vectors
% nrecs = 13679;    % Total tibobs record count = 13680
nrecs = length(Tbvcol);
SMcol = zeros(nrecs,1);
TBerrcol = zeros(nrecs,1);

% Calibrate model parameters
sand = 0.303;   % sand content (0-1)
clay = 0.099;  % clay content (0-1)
rob = 0.8;    % Soil bulk density (g/cm3)
teta = 40;  % Incidence angle (nadir = 0)
tth0 = 0.01;     % Vegetation structure parameter tth
rtt0 = 0.01;     % ttv0 =  tth0*rtt0;
omgh0 = 0.;    % vegetation scattering albedo h-pol
domg0 = 1; % omgv0 = omgh0 + domg0;
hsol0 = 0;  % Roughness parameter Hr
nsolv0 = -1;   % Roughness exponent Nr at v-pol
nsolh0 = 1;   % Roughness exponent Nr at h-pol
qsol0 = 1;    % Polarization mixing parameter Qr
ret = 0.01;    % initial soil moisture value [v/v]
%b1s = 0.12;    % tau-LAI proportionality constant

% SM retreival
for i = 1:nrecs
    
    tauh0 = 0.01; %b1s*lai(i);  % Veg. optical depth at NADIR =  b1s*LAI + b2s (b2s set to 0)

    % Brigthness temperature (Kelvin)
    Tbv = Tbvcol(i);  % V-pol 
    Tbh = Tbhcol(i);   % H-pol 

    ts1 = 225; % stemp(i);
    ts2 = ts1; % dtemp(i);

    tc = ts1;  % Canopy temperature
    tgc0 = ts1;  % Effective ground/canopy temperature --NOT USED

    % Build input vector
    frac_parameters = [sand clay rob ts1 ts2 tc teta tauh0 tgc0 tth0 rtt0 omgh0 domg0 hsol0 qsol0 nsolv0 nsolh0];
    Call_lmeb_call(ret);
    [x,resnorm,residual,exitflag,output,lambda,jacobian] = Solver_lmeb();
    TBerrcol(i) = resnorm;
    SMcol(i) = x;
end

%disp('Root Mean Square Error (Soil Moisture): ')
%disp(compute_rmse(true_sm, SMcol));
%store_tibetan([Tbvcol, Tbhcol, stemp, dtemp, lai, true_sm, SMcol])
