function y = reflect ( teta, eps0, eps2, hsol, qsol, nsolv, nsolh)

% computes surface reflectivity from Fresnel coefficients
% teta = incidence angle (degree)

% **** init


rd=180/pi;

% **********************************
% *** calcul de reflsol

muv=cos(teta/rd);

cc0=muv+0.i;
cs0=sqrt(1.-cc0.*cc0);
cs2=cs0.*sqrt(eps0./eps2);
cc2=sqrt(1.-cs2.*cs2);

% *** refl 0/2
cx=sqrt(eps0)*cc0-sqrt(eps2).*cc2;
cy=sqrt(eps0)*cc0+sqrt(eps2).*cc2;
refh=cx./cy;
cx=sqrt(eps2)*cc0-sqrt(eps0)*cc2;
cy=sqrt(eps2)*cc0+sqrt(eps0)*cc2;
refv=cx./cy;

rv20=abs(refv).*abs(refv);
rh20=abs(refh).*abs(refh);


% **********************************
% *** 	Rugosite de Choudhury

yyv=exp(-hsol*(muv.^nsolv));
yyh=exp(-hsol*(muv.^nsolh));
rv20r=((1-qsol)*rv20+qsol*rh20).*yyv;
rh20r=((1-qsol)*rh20+qsol*rv20).*yyh;


% **********************************
% ***   Calcul de TB sol
%tbsv=(1-rv20r).*t2eff +rv20r.*tbsky;
%tbsh=(1-rh20r).*t2eff +rh20r.*tbsky;

% !!! SORTIE DE LA FONCTION
%y=[tbsv;tbsh];
y=[rv20r; rh20r];

