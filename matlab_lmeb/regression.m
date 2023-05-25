function [q,rmse]=regression(x,y,n)
   % a intercept
   % b slope
   % correlation coeffiicient
   % n degree of fitting polynom
   % rmse of differences between data points and regression
     
q=polyfit(x,y,n);
rmse=sqrt((sum((polyval(q,x)-y).^2))/length(y));
% corr=corrcoef(x,y).^2;