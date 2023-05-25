       function tsky=skytl(teta, zz, t2m, q2m, rr)

%  SUB:SKYTL      calcul de Tsky at L-band     (ref: Pellerin et al., 2003)
%   input: 
%   ouput : tsky (=total (sky + atmosphere) downwelling radiation at surface level
%    tauat=atmosphere zenith opacity 
%    gossat=atmospheric loss factor: gossat = exp ( -tauat / cos(teta0))

%	zz	Altitude of the surface (derived from the surface pressure field)	km
%	T2m	Surface (screen level) air temperature	K
%	Q2m	Surface (screen level) air specific humidity	g kg-1  (vary between 0 to 25; dry ~ 5)
%	RR	Rain rate	mm h-1

rd=180/pi;
tcos=2.7;
xmuv0=cos(teta/rd);


tauat = exp( -4.011 - 0.2193 * zz - 0.00334 *t2m + 0.0145 * rr);
taeq = exp(5.051 + 0.001727 * t2m + 0.00192 * q2m - 0.0069 *zz);

gossat=exp(-tauat./xmuv0);
tsky=taeq.*(1. - gossat) + tcos .* gossat;
