%  SUB:WANG  calcul cte dielectrique du sol (Wang&Schmugge(80))
%    entree: f,T2,xmv transition, gamma
%            sand,clay,rob,xmvsol,salsol(salinite)
%            ros=2.66g/cm3
%            sand,clay = fraction de sand et clay
%            rob:g/cm3,mv(cm3/cm3),salsol:salinite eau du sol(0/00)
%    sortie: epsol
%       if(freq.ge.18.) call wang(f,tsol,0.17,1.3,epsol)
% !!!
%       avec f=freq*1.E9 (Hz) et tsol en K

       function epsol=wang(f,t2,xmvt,seff,sand,clay,rob,xmvsol)

       salsol=0.738;
       ros=2.66;
       epwi=4.9;
       epice=3.2+i*0.1;
       eps=5.5+i*0.2;
       ts=t2-273.15;
       permit=8.854e-12;
       freq=f*1.e-9;

       if freq<30  
       gam=0.60;
       elseif (freq>=30)&(freq<60)  
       gam=0.81;
       elseif (freq>=60) gam=1.19;
       end

      xa=1+1.613e-5*ts*salsol-3.656e-3*salsol...
      +3.21e-5*salsol*salsol-4.232e-7*(salsol^3);
       epw0=xa*(87.134-1.949e-1*ts-1.276e-2*ts*ts+2.491e-4*(ts^3));
       xb=1+2.282e-5*ts*salsol-7.638e-4*salsol ...
      -7.76e-6*salsol*salsol+1.105e-8*(salsol^3);
       topi=xb*(1.1109e-10-3.824e-12*ts+6.938e-14*ts*ts ...
      -5.096e-16*(ts^3));

       cx=(epw0-epwi)/(1+i*topi*f);
       epfw=epwi+cx-i*seff*(ros-rob)/(2*pi*f*permit*ros*xmvsol);
       epfwt=epwi+cx-i*seff*(ros-rob)/(2*pi*f*permit*ros*xmvt);

	if xmvsol<=xmvt
	ex=epice+(epfw-epice)*gam*xmvsol/xmvt;
	epsol=1+rob*(eps-1)/ros+xmvsol*(ex-1);
	else
	ex=epice+(epfw-epice)*gam;
	epsol=1+rob*(eps-1)/ros+xmvt*(ex-epfw)+xmvsol*(epfw-1);
	end

       return

       

