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

    # Dobson Calibration
    dob_dict = {
        'p_s': 2.664,
        'eps_sld': 4.7,
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

            # Using Dobson (1995)
            def get_permittivity():
                pass

            def get_reflectivity():
                pass

            def get_optical_depth():
                pass

            def get_roughness_params():
                pass

            

            # Optical Depth
            tau_veg = (b1s * lai * b2s) * \
                (tt * np.sin(theta)**2 + np.cos(theta)**2)
            tau = tau_veg + tau_lit + tau_inc

            # Reflectivity
            refl_fresnel = 
            refl_gr = refl_fresnel*np.exp(-hret*np.cos(theta))

            # Roughness
            hret = p['sand'] - p['clay']*p['sm_ret']

            # Temperature
            c_t = (p['sm_ret']/p['w0'])**p['bw0']
            # Choudhary et al. (1982)
            temp_gr = p['tdept'] + c_t*(p['tsurf'] - p['tdept'])

            # Putting it all together
            gamma = np.exp(-tau / np.cos(theta))
            tb = (1 - omega)*(1 - gamma)*(1 + gamma*refl_gr) * \
                temp_cp + (1-refl_gr)*gamma*temp_gr

    