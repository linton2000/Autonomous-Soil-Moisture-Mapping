from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from schema import tibetan_data_df_schm, csv2_df_schm
import pandas as pd

class ParamHandler:

    def __init__(self) -> None:
        # Apach Spark (Data Extraction, Processing & ML engine) initialization
        self.spark: SparkSession = SparkSession.builder.master('local[*]')\
                                                       .appName('SM Retreival App').getOrCreate()
        self.spark.sparkContext.setLogLevel('ERROR')

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
    
    def load_tibetan_csv_data(self, csv1: str, csv2: str):
        # Reading CSV Files
        self.data_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                      .schema(tibetan_data_df_schm).load(csv1)
        csv2_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                 .schema(csv2_df_schm).load(csv2)

        # Extracting needed columns
        data_cols = ['Datetime', 'TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', \
                     'TBH_55', 'TBV_55', 'TBH_60', 'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70']
        self.data_df = self.data_df.select(data_cols)

        # Calculating Avg. Soil Moisuture & Temp for data df
        @F.udf
        def avg_func(cols):
            res, count = 0, 0
            for cl in cols:
                if cl is not None:
                    res += cl
                    count += 1
            return res/count
        
        csv2_df = csv2_df.withColumn('Avg_SM_LC', avg_func(F.array(csv2_df.columns[1:21])).cast('float'))\
                         .withColumn('Avg_STS_LC', avg_func(F.array(csv2_df.columns[21:24])).cast('float'))\
                         .withColumn('Avg_STD_LC', avg_func(F.array(csv2_df.columns[24:])).cast('float'))\
                         .withColumnRenamed('Datetime', 'Datetime_LC')\
                         .select('Datetime_LC', 'Avg_SM_LC', 'Avg_STS_LC', 'Avg_STD_LC')

        # Joining Measured data with corresponding validation data
        self.data_df = self.data_df.join(csv2_df, self.data_df['Datetime']==csv2_df['Datetime_LC'], how='inner')
        self.data_df = self.data_df.select([cl for cl in self.data_df.columns if cl != 'Datetime_LC'])

    def _count_null(df):
        return df.select([F.count(F.when(F.col(c).isNull() | F.isnan(c), c)).alias(c) for c in df.columns])

    def print_data_df(self):
        print(f'\nNo. of Records in data_df: {self.data_df.count()}')
        print('\nSchema:')
        self.data_df.printSchema()
        # Using Pandas to display all columns neatly
        pd.set_option('display.max_columns', None)
        data_pdf = self.data_df.toPandas()
        null_pdf = ParamHandler._count_null(self.data_df).toPandas()
        print('\nContents:')
        print(data_pdf)
        print('\nColumn Null Counts:')
        print(null_pdf)
        print('\nStatistical Summary:')
        print(data_pdf.describe())