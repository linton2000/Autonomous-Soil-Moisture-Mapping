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
        return self.params.param_dict['sand']