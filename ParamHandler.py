from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as F
from IPython.display import display

class ParamHandler:
    tibetan_data_df_schm = StructType([
        StructField('Datetime', TimestampType(), True),
        # Temperature Brightness - dual-polarised at incident angles: 45, 50, 55, 60, 65 & 70
        StructField('TBH_40', FloatType(), True),
        StructField('TBV_40', FloatType(), True),
        StructField('TBH_45', FloatType(), True),
        StructField('TBV_45', FloatType(), True),
        StructField('TBH_50', FloatType(), True),
        StructField('TBV_50', FloatType(), True),
        StructField('TBH_55', FloatType(), True),
        StructField('TBV_55', FloatType(), True),
        StructField('TBH_60', FloatType(), True),
        StructField('TBV_60', FloatType(), True),
        StructField('TBH_65', FloatType(), True),
        StructField('TBV_65', FloatType(), True),
        StructField('TBH_70', FloatType(), True),
        StructField('TBV_70', FloatType(), True),
        # Average Soil Moisture & Temperature values for in-situ sensors LC & Z
        StructField('Avg_SM_LC', FloatType(), True),
        StructField('Avg_SM_Z', FloatType(), True),
        # Surface Temperature (2-5cm)
        StructField('Avg_STS_LC', FloatType(), True),
        StructField('Avg_STS_Z', FloatType(), True),
        # Average Temp. at Depth (5cm+)
        StructField('Avg_STD_LC', FloatType(), True),
        StructField('Avg_STD_Z', FloatType(), True),
    ])

    csv2_df_schm = StructType([
        StructField('Datetime', TimestampType(), True),
        StructField('SM2_5_1', FloatType(), True),
        StructField('SM2_5_2', FloatType(), True),
        StructField('SM05', FloatType(), True),
        StructField('SM7_5', FloatType(), True),
        StructField('SM10', FloatType(), True),
        StructField('SM12_5', FloatType(), True),
        StructField('SM15', FloatType(), True),
        StructField('SM17_5', FloatType(), True),
        StructField('SM20', FloatType(), True),
        StructField('SM25', FloatType(), True),
        StructField('SM30', FloatType(), True),
        StructField('SM35', FloatType(), True),
        StructField('SM40', FloatType(), True),
        StructField('SM45', FloatType(), True),
        StructField('SM50', FloatType(), True),
        StructField('SM60', FloatType(), True),
        StructField('SM70', FloatType(), True),
        StructField('SM80', FloatType(), True),
        StructField('SM90', FloatType(), True),
        StructField('SM100', FloatType(), True),
        StructField('ST2_5_1', FloatType(), True),
        StructField('ST2_5_2', FloatType(), True),
        StructField('ST05', FloatType(), True),
        StructField('ST7_5', FloatType(), True),
        StructField('ST10', FloatType(), True),
        StructField('ST12_5', FloatType(), True),
        StructField('ST15', FloatType(), True),
        StructField('ST17_5', FloatType(), True),
        StructField('ST20', FloatType(), True),
        StructField('ST25', FloatType(), True),
        StructField('ST30', FloatType(), True),
        StructField('ST35', FloatType(), True),
        StructField('ST40', FloatType(), True),
        StructField('ST45', FloatType(), True),
        StructField('ST50', FloatType(), True),
        StructField('ST60', FloatType(), True),
        StructField('ST70', FloatType(), True),
        StructField('ST80', FloatType(), True),
        StructField('ST90', FloatType(), True),
        StructField('ST100', FloatType(), True),
    ])

    csv3_df_schm = StructType([
        StructField('Datetime', TimestampType(), True),
        StructField('SM05', FloatType(), True),
        StructField('SM10', FloatType(), True),
        StructField('SM20', FloatType(), True),
        StructField('SM40', FloatType(), True),
        StructField('SM80', FloatType(), True),
        StructField('SM160', FloatType(), True),
        StructField('ST05', FloatType(), True),
        StructField('ST10', FloatType(), True),
        StructField('ST20', FloatType(), True),
        StructField('ST40', FloatType(), True),
        StructField('ST80', FloatType(), True),
        StructField('ST160', FloatType(), True),
    ])

    def __init__(self) -> None:
        self.spark: SparkSession = SparkSession.builder.master('local[*]')\
                                                       .appName('SM Retreival App').getOrCreate()
        self.spark.sparkContext.setLogLevel('ERROR')
        # Measured Data
        self.data_df = self.spark.createDataFrame(
            data=self.spark.sparkContext.emptyRDD(), schema=ParamHandler.tibetan_data_df_schm)
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
    
    def load_tibetan_csv_data(self, csv1: str, csv2: str, csv3: str):
        csv1_cols = ['Datetime', 'TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', \
                     'TBH_55', 'TBV_55', 'TBH_60', 'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70']
        
        self.data_df = self.spark.read.csv(csv1, header=True).select(csv1_cols)
        csv2_df = self.spark.read.csv(csv2, header=True, schema=ParamHandler.csv2_df_schm)
        csv3_df = self.spark.read.csv(csv3, header=True, schema=ParamHandler.csv3_df_schm)

        display(self.data_df.toPandas())
        # Calculating Avg. Soil Moisuture & Temp for data df
        avg_func = F.udf(lambda cols: F.sum(cols)/len(cols), FloatType())
        csv2_df = csv2_df.withColumn('Avg_SM_LC', avg_func(F.array(csv2_df.columns[1:21])))\
                         .withColumn('Avg_STS_LC', avg_func(F.array(csv2_df.columns[21:24])))\
                         .withColumn('Avg_STD_LC', avg_func(F.array(csv2_df.columns[24:])))\
                         .withColumnRenamed('Datetime', 'Datetime1')\
                         .select('Datetime1', 'Avg_SM_LC', 'Avg_STS_LC', 'Avg_STD_LC')
        csv3_df = csv3_df.withColumn('Avg_SM_Z', avg_func(F.array(csv3_df.columns[7:])))\
                         .withColumn('Avg_STD_Z', avg_func(F.array(csv3_df.columns[2:7])))\
                         .withColumn('Avg_STS_Z', F.col(csv3_df.columns[1]))\
                         .withColumnRenamed('Datetime', 'Datetime2')\
                         .select('Datetime2', 'Avg_SM_Z', 'Avg_STS_Z', 'Avg_STD_Z')
        
        self.data_df = self.data_df.join(csv2_df, self.data_df['Datetime']==csv2_df['Datetime1'], how='inner')
        #self.data_df = self.data_df.join(csv3_df, self.data_df['Datetime']==csv3_df['Datetime2'], how='inner')
        #self.data_df = self.data_df.select([cl for cl in self.data_df.columns if cl not in ['Datetime1', 'Datetime2']])

    def print_data_df(self):
        display(self.data_df.toPandas())
        """ self.data_df.printSchema()
        self.data_df.summary().show()
        print(self.data_df.count)
        self.data_df.select([F.count(F.when(F.isnan(c) | F.col(c).isNull(), c)).alias(c) for c in self.data_df.columns]).show() """