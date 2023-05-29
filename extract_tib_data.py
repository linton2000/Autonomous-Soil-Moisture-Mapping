from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType, FloatType
from schema import tibetan_data_df_schm, val_df_schm

if __name__ == '__main__':
    # Initialising Spark
    root_dir = '/Users/lintoncharles/Documents/University/FIT4701_2/code/Autonomous-Soil-Moisture-Mapping/'
    spark = SparkSession.builder\
                        .master('local[*]')\
                        .appName('SM Retreival App')\
                        .config('spark.sql.warehouse.dir', root_dir)\
                        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')

    # Reading CSV Files
    mes_csv = 'selected_tibobs_data/TB_measurement_data.csv'
    val_csv = 'selected_tibobs_data/SM_temp_validation_data.csv'
    lai_csv = 'selected_tibobs_data/LAI_processed_modis_data.csv'

    data_df = spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                  .schema(tibetan_data_df_schm).load(mes_csv)
    val_df = spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
        .schema(val_df_schm).load(val_csv)
    lai_df = spark.read.format('csv').options(header=True, multiline=True, inferSchema=True).load(lai_csv)
    
    # Extracting needed columns
    data_cols = ['Datetime', 'TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50',
                 'TBH_55', 'TBV_55', 'TBH_60', 'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70']
    data_df = data_df.select(data_cols)

    # Calculating Avg. Soil Moisuture & Temp for data df
    @F.udf
    def avg_func(cols):
        res, count = 0, 0
        for cl in cols:
            if cl is not None:
                res += cl
                count += 1
        return res/count
    
    # Computing average SM, surface temp. (STS - 5cm) and ground temp. (STD - 5cm+) 
    val_df = val_df.withColumn('Avg_SM_LC', avg_func(F.array(val_df.columns[1:21])).cast('float'))\
        .withColumn('Avg_STS_LC', avg_func(F.array(val_df.columns[21:24])).cast('float'))\
        .withColumn('Avg_STD_LC', avg_func(F.array(val_df.columns[24:])).cast('float'))\
        .withColumnRenamed('Datetime', 'Datetime_LC')\
        .select('Datetime_LC', 'Avg_SM_LC', 'Avg_STS_LC', 'Avg_STD_LC')
    
    # Joining Measured data with corresponding validation & lai data
    data_df = data_df.join(
        val_df, data_df['Datetime'] == val_df['Datetime_LC'], how='inner')
    
    lai_df = lai_df.withColumnRenamed('Datetime', 'Datetime_LAI')
    data_df = data_df.join(
        lai_df, data_df['Datetime'] == lai_df['Datetime_LAI'], how='inner')
    
    # Ssaving to tibobs_data.csv
    data_df.write.option("header",True)\
                 .option("delimiter","|")\
                 .csv("combined_tibobs")