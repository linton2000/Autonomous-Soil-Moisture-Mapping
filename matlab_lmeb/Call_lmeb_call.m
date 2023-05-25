function [cf] = Call_lmeb_call(ret)
% this functions is called by "Solver_lmeb"
% to do soil moisture retrieval. It takes a soil moisture guess "ret"
% passed by "Solver_lmeb", applies L-MEB (routine "lmeb_call_cmplx") to calculate
% the simulated brightness temperatures (tbsim) and calculates
% the squared sum of the differences between tbsim and the observed
% brightness temperatures (tbobs)

%#ok<*GVMIS>
global conf;
res = [];

% evaluate input arrays  from base workspace
yobsv = evalin('base','Tbv');
yobsh = evalin('base','Tbh');
param = evalin('base','frac_parameters');
conf = [0, 0, 0];  % [disp_params, show_plt, disp_regr]

[ysim, autres] = lmeb_call(ret, param);
ysimv = ysim(1);
ysimh = ysim(2);

tbobs = horzcat(yobsv,yobsh);
tbsim = horzcat(ysimv,ysimh);

%*************************************************************************
% Calculate cost function
% cf = sum((yobs-Tbsim).^2);
%*************************************************************************
cf = tbobs-tbsim;  % the algorithm implicitly squares and sums elements of array cf