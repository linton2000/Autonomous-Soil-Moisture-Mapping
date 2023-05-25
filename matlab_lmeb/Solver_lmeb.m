function [x,resnorm,residual,exitflag,output,lambda,jacobian] = Solver_lmeb

% This functions is called by "Input_lmeb"
% to perform least square optimization of L-MEB
% brigthness temperatures using MATLAB function "lsqnonlin"
% which solve nonlinear least-squares problems.

% It calls function "Call_lmeb_call" to calculate L-MEB brightness
% temperatures given a soil moisture guess.


% Start with the default options
options = optimset;
% Modify options setting
options = optimset(options,'Display' ,'on');
options = optimset(options,'LargeScale' ,'on');
% options = optimset(options,'TolFun' ,0.01);
% options = optimset(options,'TolX' ,0.001);
options = optimset(options,'MaxFunEvals' ,10000);
% options = optimset(options,'LevenbergMarquardt' ,'on');
[x,resnorm,residual,exitflag,output,lambda,jacobian] = ...
lsqnonlin(@Call_lmeb_call,0.1,0,0.5,options);
