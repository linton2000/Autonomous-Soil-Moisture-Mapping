function [x,resnorm,residual,exitflag,output,lambda,jacobian] = solver_least_squares
% This is an auto generated M-file to do optimization with the Optimization Toolbox.
% Optimization Toolbox is required to run this M-file.

% Start with the default options
options = optimset;
% Modify options setting
options = optimset(options,'Display' ,'off');
options = optimset(options,'LargeScale' ,'on');
% options = optimset(options,'TolFun' ,0.01);
% options = optimset(options,'TolX' ,0.001);
options = optimset(options,'MaxFunEvals' ,10000);
options = optimset(options,'LevenbergMarquardt' ,'on');
[x,resnorm,residual,exitflag,output,lambda,jacobian] = ...
lsqnonlin(@Optimization_LMEB,[0.5 0.1],[0 0],[1 1] ,options);
