from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from schema import tibetan_data_df_schm, csv2_df_schm
import pandas as pd
from pyspark.sql import DataFrame


class DataFrameHandler():
    def __init__(self) -> None:
        # Apache Spark (Data Extraction, Processing & ML engine) initialization
        self.spark: SparkSession = SparkSession.builder.master('local[*]')\
                                                       .appName('SM Retreival App').getOrCreate()
        self.spark.sparkContext.setLogLevel('ERROR')

    def load_tibetan_csv_data(self, csv1='TB_measurement_data.csv', csv2='SM_temp_validation_data.csv') -> None:
        # Reading CSV Files
        self.data_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                      .schema(tibetan_data_df_schm).load(csv1)
        csv2_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                 .schema(csv2_df_schm).load(csv2)

        # Extracting needed columns
        data_cols = ['Datetime', 'TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50',
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
        self.data_df = self.data_df.join(
            csv2_df, self.data_df['Datetime'] == csv2_df['Datetime_LC'], how='inner')
        self.data_df = self.data_df.select(
            [cl for cl in self.data_df.columns if cl != 'Datetime_LC'])

    def _count_null(df) -> DataFrame:
        return df.select([F.count(F.when(F.col(c).isNull() | F.isnan(c), c)).alias(c) for c in df.columns])

    def print_data_df(self) -> None:
        print(f'\nNo. of Records in data_df: {self.data_df.count()}')
        print('\nSchema:')
        self.data_df.printSchema()
        # Using Pandas to display all columns neatly
        pd.set_option('display.max_columns', None)
        data_pdf = self.data_df.toPandas()
        null_pdf = DataFrameHandler._count_null(self.data_df).toPandas()
        print('\nContents:')
        print(data_pdf)
        print('\nColumn Null Counts:')
        print(null_pdf)
        print('\nStatistical Summary:')
        print(data_pdf.describe())
