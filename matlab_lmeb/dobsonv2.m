function [er_r]=dobsonv2(fi,mv,ts,sf,cf)
%   !----------------------------------------------------------------------------
%   !  DOBSONV2  Compute the complex dielectric constant of soil as a function
%   !            of frequency, soil moisture, sand/clay fractions, and surface
%   !            temperature.  The implementation follows Ann Hsu's code on
%   !            the Dobson's model, in that only the real part of the
%   !            dielectric constant is computed.  Also, the approach starts
%   !            with fixing EPSS at 4.70 and then computes for RHOB and RHOS.
%   !            Low frequency correction is made for the real part of the
%   !            dielectric constant.  Furthermore, the (mv) is approximated
%   !            by (mv)^betar according to Ulaby's book in the expression of
%   !            the real part of the dielectric constant.
%   !
%   !            Ann Hsu can be contacted at hsu@hydrolab.arsusda.gov
%   !
%   !            er_r  Dielectric Constant (Real Part)
%   !            fi    Frequency (GHz)
%   !            mv    Soil moisture content (g cm-3)
%   !            ts    Soil temperature (deg C)
%   !            sf    Mass fraction of sand content in soil
%   !            cf    Mass fraction of clay content in soil
%   !----------------------------------------------------------------------


  % Set physical constants and bounds
  alpha   = 0.65;       % optimized coefficient
  epso    = 8.854e-12;  % permittivity of free space (F/m)
  epswinf = 4.9;        % high-freq. limit of free watr diel. const.


  % Compute dielectric constant of soil solid particles
  epss = 4.70;
  rhos = (sqrt(epss + 0.062) - 1.01)/0.44;
  por = 0.505 - 0.142*sf - 0.037*cf;
  fv = 1 - por;
  rhob = fv*rhos;
  
  % Compute optimized coefficient values
  betar  =  1.27480 - 0.519*sf - 0.152*cf;
  
  % Compute dielectric constant of free water (expressions for
  %         relaxation time and static dielectric constant obtained from
  %         Ulaby et al., Vol. 3)
  omtau  =  fi*(1.1109e-1 - 3.824e-3*ts + 6.938e-5*ts^2 - 5.096e-7*ts^3);
  epswo  =  88.045 - 0.4147*ts + 6.295e-4*ts^2 + 1.075e-5*ts^3;
  fac    = (epswo - epswinf) / (1.0 + omtau^2);
  epsfwr =  epswinf + fac;
  er_r   = (1+(epss^alpha-1)*rhob/rhos+(mv.^betar).*((epsfwr.^alpha)-1))^(1/alpha)


  % Correction factor (Peplinski et al., 1995)
  if fi < 1.4
      er_r = 1.15*er_r - 0.68
  end