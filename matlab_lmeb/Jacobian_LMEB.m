function [out]=Jacobian_LMEB(sm);
deltasm=0.005;
% Calculate Jacobian by finite differences
% using MATLAB function sfdnls.m
%-------------------------------------
% Rocco Panciera 06/2008
%-------------------------------------
% sm: sm at which calculate jacobian

DiffMinChange = 1.0000e-008;  % smallest finite increment
DiffMaxChange = 0.1000;       % bigger finite increment
Jstr = sparse(ones(2,1));  % Jstr: Sparsity of Jacobian
group=1;      %indicates how to use sparse finite differencing: group(i) = j 
              % means that column i belongs to group (or color) j. Each group (or color) 
              % corresponds to a function difference.
varargin={};    % eventual extra-input of function @Forward_LMEB
alpha=[];   % A non-empty input alpha overrides the default finite
            % differencing stepsize(=1.4901e-008, srqt of MATLAB floating-point relative
            % accuracy)
          

f1 = feval(@Forward_LMEB,sm,varargin{:}) ;  %LMEB calculated at sm
f2 = feval(@Forward_LMEB,sm+deltasm,varargin{:}) ;  %LMEB calculated at sm+delta_SM
out(1)=f1(1); %Operation function h(x) at V-pol
out(2)=f1(2); %Operation function h(x) at H-pol

out(3)=(f2(1)-f1(1))/deltasm; %Jacobian at V-pol
out(4)=(f2(2)-f1(2))/deltasm;  %Jacobian at H-pol

%[J] = sfdnls(sm,fval,Jstr,group,alpha,DiffMinChange, DiffMaxChange,@Forward_LMEB,[],[],varargin{:});