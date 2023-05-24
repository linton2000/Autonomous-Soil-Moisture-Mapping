import numpy as np
from ParamHandler import ParamHandler
from Regressor import Regressor


class LMEBRegressor(Regressor):
    # Tibetan Study Calibrated Values
    tib_dict = {
        'sand': 0.303,
        'clay': 0.099,
    }
    # Wigneron et al. L-MEB Calibration
    wig_dict = {
        'w0': 0.3,
        'bw0': 0.3
    }

    # Dobson Parameters
    dob_dict = {
        'rhos': 2.664,
        'eps_sld': 4.7,
        'eps_whf': 4.9,
        'eps_free': 8.854e-12,
        'dob_alpha': 0.65,
    }

    def __init__(self, params: ParamHandler) -> None:
        self.params = params

    def fit(self) -> None:
        for dct in [LMEBRegressor.tib_dict, LMEBRegressor.wig_dict, LMEBRegressor.dob_dict]:
            self.params.patch_dict(LMEBRegressor.dob_dict)
        return self._simulate_TB()

    def _simulate_TB(self):
        p = self.params.param_dict
        theta = p['theta']
        for p in ['h', 'v']:
            # Initialisation
            tt, omega, tb_sky = [0]*3
            b1s, b2s, lai = p['b1s'], p['b2s'], p['lai']
            tau_lit, tau_inc = p['tau_lit'], p['tau_inc']
            if p == 'h':
                tt = p['tth']
                omega = p['omgh']
                tb_sky = p['tb_skyH']
            else:
                tt = p['ttv']
                omega = p['omgv']
                tb_sky = p['tb_skyV']

            # Dobson et al (1995 & 1985)
            def get_permittivity():
                sm, rhos, rhob, eps_sld, alpha = p['sm_ret'], p['rhos'], p['rhob'], p['eps_sld'], p['dob_alpha']
                sand, clay, eps_whf, es0 = p['sand'], p['clay'], p['eps_whf'], p['eps_free']

                # Soil texture dependent co-efficients
                b1 = (127.48 - 0.519*sand - 0.152*clay)/100
                b2 = (1.33797 - 0.603*sand - 0.166*clay)/100
                sge = 1.645 + 1.939*rhob - 0.02013*sand + 0.01594*clay

                # Ulaby et al., vol 3 (source: Ann Hsu's dobson script)
                _, ts = get_temperature()
                f = 1.41e9    # Frequency in Hz
                # Water Static dielectric const.
                eps_w0 = 88.045 - 0.4147*ts + 6.295e-4*ts ^ 2 + 1.075e-5*ts ^ 3
                # Water relaxation time
                rel_time = 1.41*(1.1109e-1 - 3.824e-3*ts +
                                 6.938e-5*ts ^ 2 - 5.096e-7*ts ^ 3)

                # Dielectric Constant of Soil Free water
                eps_fwr = eps_whf + ((eps_w0 - eps_whf) /
                                     (1 + (2*np.pi*f*rel_time)**2))
                eps_fwi1 = (2*np.pi*f*rel_time*(eps_w0-eps_whf)) / \
                    (1 + (2*np.pi*f*rel_time)**2)
                eps_fwi = eps_fwi1 + \
                    (sge/(2*np.pi*f*eps_w0))*((rhos-rhob)/(rhos*sm))

                # Soil dielectric constant aka permittivity
                eps_real = (1 + (rhob/rhos)*(eps_sld**alpha - 1) +
                            (sm**b1)*(eps_fwr**alpha) - sm)**(1/alpha)
                eps_cplx = ((sm**b2)*(eps_fwi**alpha))**(1/alpha)
                return complex(eps_real, eps_cplx)

            def get_reflectivity():
                refl_fresnel = 0
                return refl_fresnel*np.exp(-hret*np.cos(theta))

            def get_optical_depth():
                tau_veg = (b1s * lai * b2s) * \
                    (tt * np.sin(theta)**2 + np.cos(theta)**2)
                return tau_veg + tau_lit + tau_inc

            def get_roughness_params():
                hret = p['sand'] - p['clay']*p['sm_ret']

            # Choudhary et al. (1982)
            def get_temperature():
                c_t = (p['sm_ret']/p['w0'])**p['bw0']
                temp_gr = p['tdept'] + c_t*(p['tsurf'] - p['tdept'])
                temp_cp = 0
                return temp_cp, temp_gr

            # Putting it all together
            tau = get_optical_depth()
            refl_gr = get_reflectivity()
            temp_cp, temp_gr = get_temperature()

            gamma = np.exp(-tau / np.cos(theta))
            tb = (1 - omega)*(1 - gamma)*(1 + gamma*refl_gr) * \
                temp_cp + (1-refl_gr)*gamma*temp_gr
