function [rs]=myregr(x,y)
%MYREGR: Perform a least-squares linear regression.
%This function computes a least-square linear regression suppling several
%output information.
%
% Syntax: 	myregr(x,y)
%      
%     Inputs:
%           X - Array of the independent variable 
%           Y - Array of the dependent variable
%           verbose - Flag to display all information (default=1)
%     Outputs:
%           - Slope with standard error an 95% C.I.
%           - Intercept with standard error an 95% C.I.
%           - Pearson's Correlation coefficient with 95% C.I. and its
%             adjusted form (depending on the elements of X and Y arrays)
%           - Spearman's Correlation coefficient
%           - Regression Standard Error
%           - Total Variability
%           - Variability due to regression
%           - Residual Variability
%           - Student's t-Test on Slope (to check if slope=0)
%           - Student's t-Test on Intercept (to check if intercept=0)
%           - Power of the regression
%           - a plot with:
%                o Data points
%                o Least squares regression line
%                o Red dotted lines: 95% Confidence interval of regression
%                o Green dotted lines: 95% Confidence interval of new y 
%                                       evaluation using this regression.
%
%   [Slope]=myregr(...) returns a structure of slope containing value, standard
%   error, lower and upper bounds 95% C.I.
%
%   [Slope,Intercept]=myregr(...) returns a structure of slope and intercept 
%   containing value, standard error, lower and upper bounds 95% C.I.
%
% Example:
%       x = [1.0 2.3 3.1 4.8 5.6 6.3];
%       y = [2.6 2.8 3.1 4.7 4.1 5.3];
%
%   Calling on Matlab the function: 
%             myregr(x,y)
%
%   Answer is:
%
%                         Slope
% -----------------------------------------------------------
%      Value          S.E.                95% C.I.  
% -----------------------------------------------------------
%    0.50107        0.09667        0.23267        0.76947
% -----------------------------------------------------------
%  
%                       Intercept
% -----------------------------------------------------------
%      Value          S.E.                95% C.I.  
% -----------------------------------------------------------
%    1.83755        0.41390        0.68838        2.98673
% -----------------------------------------------------------
%  
%             Pearson's Correlation Coefficient
% -----------------------------------------------------------
%      Value               95% C.I.                  ADJ  
% -----------------------------------------------------------
%    0.93296        0.49988        0.99281        0.91620
% -----------------------------------------------------------
% Spearman's Correlation Coefficient: 0.9429
%
%                       Other Parameters
% ------------------------------------------------------------------------
%      R.S.E.                         Variability  
%      Value        Total            by regression           Residual  
% ------------------------------------------------------------------------
%    0.44358        6.07333        5.28627 (87.0407%)     0.78706 (12.9593%)
% ------------------------------------------------------------------------
%
% Student's t-test on slope=0
% ----------------------------------------------------------------
% t = 5.1832    Critical Value = 2.7764     p = 0.0066
% Test passed: slope ~= 0
% ----------------------------------------------------------------
%  
% Student's t-test on intercept=0
% ----------------------------------------------------------------
% t = 4.4396    Critical Value = 2.7764     p = 0.0113
% Test passed: intercept ~= 0
% ----------------------------------------------------------------
%  
% Power of regression
% ----------------------------------------------------------------
% alpha = 0.05  n = 6     Zrho = 1.6807  std.dev = 0.5774
% Power of regression: 0.6046
% ----------------------------------------------------------------
%
% ...and the plot, of course.
%
% SEE also myregrinv, myregrcomp
%
%           Created by Giuseppe Cardillo
%           CEINGE - Advanced Biotechnologies
%           Via Comunale Margherita, 482
%           80145
%           Napoli - Italy
%           cardillo@ceinge.unina.it

%Input error handling
if any(size(x)~=size(y))
  error('X and Y arrays must have the same length.');
end

if nargin==2
    verbose=1;
end

x=x(:); y=y(:); %columns vectors
xtmp=[x ones(length(x),1)]; %input matrix for regress function
ytmp=y;

%regression coefficients
[p,pINT,R,Rint] = regress(ytmp,xtmp);

%check the presence of outliers
outl=find(ismember(sign(Rint),[-1 1],'rows')==0);
if ~isempty(outl) 
    fprintf('These points are outliers at 95%% fiducial level: %d \n',outl);
    reply = input('Do you want to delete outliers? Y/N [Y]: ', 's');
    if isempty(reply) || upper(reply)=='Y'
        ytmp(outl)=[]; xtmp(outl,:)=[];
        [p,pINT,R] = regress(ytmp,xtmp);
    end
end

xtmp(:,2)=[]; %delete column 2
%save coefficients value
m(1)=p(1); q(1)=p(2);

n=length(xtmp); 
xm=mean(xtmp); xsd=std(xtmp);

%regression standard error (RSE)
RSE=realsqrt((sum(R.^2))/(n-2)); %RSE

%standard error of regression coefficients
cv=tinv(0.975,n-2); %Student's critical value
m(2)=(pINT(3)-p(1))/cv; %slope standard error
m=[m pINT(1,:)]; %add slope 95% C.I.
q(2)=(pINT(4)-p(2))/cv; %intercept standard error
q=[q pINT(2,:)]; %add intercept 95% C.I.

%Pearson's Correlation coefficient
[rp,pr,rlo,rup]=corrcoef(xtmp,ytmp);
r(1)=rp(2); r(2)=rlo(2); r(3)=rup(2); 
%Adjusted Pearson's Correlation coefficient
r(4)=sign(r(1))*(abs(r(1))-((1-abs(r(1)))/(n-2)));

%Spearman's Correlation coefficient
[rx]=tiedrank(xtmp);
[ry]=tiedrank(ytmp);
d=rx-ry;
rs=1-(6*sum(d.^2)/(n^3-n));

