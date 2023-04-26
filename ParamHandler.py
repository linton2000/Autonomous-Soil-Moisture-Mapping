from pyspark.sql import SparkSession
from pyspark.sql.types import *


class ParamHandler:
    def __init__(self) -> None:
        spark = SparkSession.builder.master(
            'local[*]').appName('SM Retreival App').getOrCreate()
        data_df_schm = StructType([
            StructField('datetime', TimestampType(), True),
            # Temperature Brightness - dual-polarised at incident angles: 45, 50, 55, 60, 65 & 70
            StructField('TB_H40', FloatType(), True),
            StructField('TB_V40', FloatType(), True),
            StructField('TB_H45', FloatType(), True),
            StructField('TB_V45', FloatType(), True),
            StructField('TB_H50', FloatType(), True),
            StructField('TB_V50', FloatType(), True),
            StructField('TB_H55', FloatType(), True),
            StructField('TB_V55', FloatType(), True),
            StructField('TB_H60', FloatType(), True),
            StructField('TB_V60', FloatType(), True),
            StructField('TB_H65', FloatType(), True),
            StructField('TB_V65', FloatType(), True),
            StructField('TB_H70', FloatType(), True),
            StructField('TB_V70', FloatType(), True),
            # Average Soil Moisture & Temperature values for in-situ sensors LC & Z
            StructField('Avg_SM_LC', FloatType(), True),
            StructField('Avg_SM_Z', FloatType(), True),
            StructField('Avg_ST_S', FloatType(), True),   # Surface Temperature (2-5cm)
            StructField('Avg_ST_D', FloatType(), True)    # Average Temp. at Depth (5cm+)

        ])
        # Measured Data
        self.data_df = spark.createDataFrame(data=spark.sparkContext.emptyRDD(), schema=data_df_schm)
        # Variable (Retrieval) Parameters
        self.param_dict = {
            'tb_simV': 0,        # Simulated Brightness Temp. (K) for V-pol
            'tb_simH': 0,        # Simulated Brightness Temp. (K) for H-pol
            'sm_ret': 0,         # Retrieved soil moisture [v/v]

            'theta': 0,          # Incidence Angle (deg)
            'sand': 0,           # Sand (%)
            'clay': 0,           # Clay (%)
            'rob': 0,            # Soil Bulk Density (g/cm3)
            'ts1': 0,            # Surface Temperature (2-5cm)
            'ts2': 0,            # Average Temp. at Depth (5cm+)

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
            'xb': 0,             # Paramete B_t used to computed soil temp. (Wigneron et al.)
            'freq': 0,           # EM Frequency (L-band = 1.41Ghz)
            
        }