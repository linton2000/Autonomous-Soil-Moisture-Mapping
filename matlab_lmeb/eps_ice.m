% Function for calculating the relative permittivity of pure ice in the microwave region
% code downloaded from HUT site (J. Poulliainen)  - 2001

function z = eps_ice(f,T)
	
% T = temperature (K)
% f = frequency (GHz)

%	T = T + 273.15;
%	f = f/1e9;
		
	B1 = 0.0207;
	B2 = 1.16e-11;
	b = 335;
	deltabeta = exp(-10.02 + 0.0364*(T-273));
	betam = (B1/T) * ( exp(b/T) / ((exp(b/T)-1)^2) ) + B2*f^2;
	beta = betam + deltabeta;
	theta = 300 / T - 1;
	alfa = (0.00504 + 0.0062*theta)*exp(-22.1*theta);
	z = 3.1884 + 9.1e-4*(T-273);
	z = z - j*(alfa/f + beta*f);
return