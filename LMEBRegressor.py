import numpy as np
from ParamHandler import ParamHandler
from Regressor import Regressor

class LMEBRegressor(Regressor):
    tib_dict = {
        'sand': 0.303,
        'clay': 0.099,
    }
    
    def __init__(self, params: ParamHandler) -> None:
        self.params = params

    def fit(self) -> None:
        self.params.patch_dict(LMEBRegressor.tib_dict)
        return self._simulate_TB()
    
    def _simulate_TB(self):
        p = self.params.param_dict
        theta = p['theta']
        for p in ['h', 'v']:
            tt, omega = [0]*2
            b1s, b2s, lai = p['b1s'], p['b2s'], p['lai']
            tau_lit, tau_inc = p['tau_lit'], p['tau_inc']
            if p == 'h': 
                tt = p['tth']
                omega = p['omgh']
            elif p == 'v': 
                tt = p['ttv']
                omega = p['omgv']
            else: raise Exception(f"Invalid pol value '{p}' in _simulate_TB()")

            # Total Optical Depth = Standing Vegetation + Canopy Bottom + Veg. Water Content
            tau_veg = (b1s * lai * b2s) * (tt * np.sin(theta)**2 + np.cos(theta)**2)
            tau = tau_veg + tau_lit + tau_inc

            
            gamma = np.exp(-tau / np.cos(theta))
            tb = (1 - omega)*(1 - gamma)*(1 + gamma*refl_gr)*temp_cp + (1-refl_gr)*gamma*temp_gr