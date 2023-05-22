from DataFrameHandler import DataFrameHandler


class ParamHandler:

    def __init__(self, data_opt) -> None:
        self.data_opt: str = data_opt
        self.df_handler: DataFrameHandler = DataFrameHandler()

        # Variable (Retrieval) Parameters
        self.param_dict: dict = {
            'tb_simV': 0,        # Simulated Brightness Temp. (K) for V-pol
            'tb_simH': 0,        # Simulated Brightness Temp. (K) for H-pol
            'sm_ret': 0,         # Retrieved soil moisture [v/v]

            'tb_skyV': 0,        # Measured Sky TB_V 
            'tb_skyH': 0,        # Measured Sky TB_H

            'theta': 0,          # Incidence Angle (deg)
            'sand': 0,           # Sand (percent: 0-1)
            'clay': 0,           # Clay (percent: 0-1)
            'p_b': 0,            # Soil Bulk Density (g/cm3)
            'p_s': 0,            # Soil Particle Density
            'eps_sld': 0,        # Dielectric Constant of Solid Particles (SMOS Lv. 2)

            'tauh': 0,           # Vegetation Optical Depth at Nadir
            'tth': 0,            # Vegetation Struct. Param. tth
            'rtt': 0,            # Vegetation Struct. Param. rtt
            'omgh': 0,           # vegetation scattering albedo h-pol
            'domg': 0,           # omgv = omgh + domg;
            'hsol': 0,           # Roughness parameter Hr
            'nsolv': 0,          # Roughness exponent Nr at v-pol
            'nsolh': 0,          # Roughness exponent Nr at h-pol
            'qsol': 0,           # Polarization mixing parameter Qr
            'b_js':  0,          # Vegetation parameter (Jackson)

            'xa': 0,             # Parameter A_t used to computed soil temp.
            'xb': 0,             # Parameter B_t used to computed soil temp. (Wigneron et al.)
            'freq': 0,           # EM Frequency (L-band = 1.41Ghz)
            'tsurf': 0,          # Surface Temperature (2-5cm)
            'tdept': 0,          # Average Temp. at Depth (5cm+)
            'tcanp': 0,          # Canopy Temp.

            'w0': 0,             # Semi-empirical surface temp param 1
            'bw0': 0,            # Semi-empirical surface temp param 2  (Wigneron et al.)
        }

        if self.data_opt == 'tibetan':
            self.df_handler.load_tibetan_csv_data()

    # Updating param_dict with a new subset dict
    def patch_dict(self, ndict: dict) -> dict:
        for (key, val) in ndict.items():
            self.param_dict[key] = val
        return self.param_dict

    def print_params(self):
        param_str = "\n  ".join("{0} = {1}".format(k, v)
                                for k, v in self.param_dict.items())
        print('\nParameters:\n', param_str)
