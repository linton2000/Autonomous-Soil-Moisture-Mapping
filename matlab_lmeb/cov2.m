function [covmat]=cov2(mat)
% calculates and plots variagram of ASAR soil moisture error
% product, gridded on a regular 1km grid, with distance expressed in meters.
mat=ASAR_ERROR.days11011031;

distance=[];
diff=[];
  for y=1:size(A,1)
     for x=1:size(A,2)
         k=1;
         if ~isnan(A(y,x))
       for yy=y:size(A,1)
           if y==yy
               t=x+1;
           else
               t=1;
           end
           for xx=t:size(A,2)
               if ~isnan(A(yy,xx))
               D(k)=100000*sqrt((yy*0.1-y*0.1)^2+(xx*0.1-x*0.1)^2);
               err(k)=(A(yy,xx)-A(y,x))^2;
               k=k+1;
               else continue
               end
           end
       end
         else continue
         end
   distance=horzcat(distance,D);
  diff=horzcat(diff,err);
     end
  end


covmat(r,s)=  
         
 % bin distances and calculates mean of differences within each bin
  d=1000;
%   bin=horzcat([0:2000:30000],50000)
 bin=[0*d 1.5*d 2.5*d 3.5*d 4.5*d 5.5*d 6.5*d 7.5*d 8.5*d 9.5*d 10.5*d 20*d];
  
  for i=1:length(bin)-1
      log=distance>=bin(i) & distance<bin(i+1);
      lag(i)=mean(distance(log==1));
      variance(i)=sum(diff(log==1))/(10000*length(log(log==1)));
  end
  
  % calculates lag vector and plot variiogram


   semilogx(lag,variance,'.--g')
   axis([0 20000 0 300])
  
  clear i j bin lag variance k m n       
 clear xx yy x y t k 
