from DataFrameHandler import DataFrameHandler


class ParamHandler:

    def __init__(self, data_opt) -> None:
        self.df_handler: DataFrameHandler = DataFrameHandler()

        # Variable (Retrieval) Parameters
        self.param_dict: dict = {
            'tb_simV': 0,        # Simulated Brightness Temp. (K) for V-pol
            'tb_simH': 0,        # Simulated Brightness Temp. (K) for H-pol
            'sm_ret': 0,         # Retrieved soil moisture [v/v]

            'theta': 0,          # Incidence Angle (deg)
            'sand': 0,           # Sand (%)
            'clay': 0,           # Clay (%)
            'rob': 0,            # Soil Bulk Density (g/cm3)

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

            'xa': 0,             # Paramete A_t used to computed soil temp.
            # Paramete B_t used to computed soil temp. (Wigneron et al.)
            'xb': 0,
            'freq': 0,           # EM Frequency (L-band = 1.41Ghz)
            'ts1': 0,            # Surface Temperature (2-5cm)
            'ts2': 0,            # Average Temp. at Depth (5cm+)
            'tc': 0,             # Canopy Temp.
        }

        if data_opt == 'tibetan':
            self.df_handler.load_tibetan_csv_data()

    def print_data(self, also_df=False):
        if also_df: self.df_handler.print_data_df()
        param_str = "\n  ".join("{0} = {1}".format(k, v)  for k,v in self.param_dict.items())
        print('\nParameters:\n', param_str)