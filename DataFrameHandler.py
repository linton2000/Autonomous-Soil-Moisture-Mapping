from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd
from pyspark.sql.types import DoubleType, FloatType
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from schema import tibetan_data_df_schm, val_df_schm


class DataFrameHandler():
    def __init__(self) -> None:
        # Apache Spark (Data Extraction, Processing & ML engine) initialization
        self.spark: SparkSession = SparkSession.builder.master('local[*]')\
                                                       .appName('SM Retreival App').getOrCreate()
        self.spark.sparkContext.setLogLevel('ERROR')

    def load_tibetan_csv_data(self, mes_csv='TB_measurement_data.csv', val_csv='SM_temp_validation_data.csv') -> None:
        # Reading CSV Files
        self.data_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
                                      .schema(tibetan_data_df_schm).load(mes_csv)
        val_df = self.spark.read.format('csv').options(header=True, multiline=True, inferSchema=True)\
            .schema(val_df_schm).load(val_csv)

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

        val_df = val_df.withColumn('Avg_SM_LC', avg_func(F.array(val_df.columns[1:21])).cast('float'))\
            .withColumn('Avg_STS_LC', avg_func(F.array(val_df.columns[21:24])).cast('float'))\
            .withColumn('Avg_STD_LC', avg_func(F.array(val_df.columns[24:])).cast('float'))\
            .withColumnRenamed('Datetime', 'Datetime_LC')\
            .select('Datetime_LC', 'Avg_SM_LC', 'Avg_STS_LC', 'Avg_STD_LC')

        # Joining Measured data with corresponding validation data
        self.data_df = self.data_df.join(
            val_df, self.data_df['Datetime'] == val_df['Datetime_LC'], how='inner')
        self.data_df = self.data_df.withColumn('Datetime', F.to_timestamp('Datetime', 'M/d/yyyy H:mm'))\
                                   .drop('Datetime_LC')

    def _count_nulls(self):
        null_df = self.data_df.select([F.count(F.when(F.isnan(c) | F.isnull(c), c)).alias(
            c) for (c, c_type) in self.data_df.dtypes if c_type not in ('timestamp', 'string', 'date')])
        return null_df

    def print_data_df(self, show_all=False, show_numRecs=False, show_nulls=False, show_stats=False, show_schm=False,
                      show_table=False) -> None:
        if show_all:
            show_numRecs, show_nulls, show_stats, show_schm, show_table = [
                True]*5
        if show_numRecs:
            print(f'\nNo. of Records in data_df: {self.data_df.count()}')
        if show_schm:
            print('\nSchema:')
            self.data_df.printSchema()
        if show_table:
            # Using Pandas to display all columns neatly
            pd.set_option('display.max_columns', None)
            data_pdf = self.data_df.toPandas()
            print('\nContents:')
            print(data_pdf)
        if show_nulls:
            print('\nNull Counts:')
            print(DataFrameHandler._count_nulls(self).toPandas())
        if show_stats:
            print('\nStatistical Summary:')
            print(data_pdf.describe())

    # Date format: yyyy-MM-dd
    def plot_TB_time(self, min_date='2016-09-01', max_date='2016-10-01', TB_angles=[40, 45]):
        # Filter dataframe for date range
        data_df = self.data_df.filter((F.to_date(F.col("Datetime")) >= min_date) & (
            F.to_date(F.col("Datetime")) <= max_date))

        # Configure matplotlib for legible x-axis datetime markings
        ax = plt.gca()
        ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MONDAY))
        ax.xaxis.set_minor_locator(DayLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%d %b %y'))
        plt.xticks(rotation=45)

        for theta in TB_angles:
            # Compute Daily values
            pdf = data_df.groupBy(F.to_date("Datetime").alias("Date"))\
                            .agg(F.avg(f"TBH_{theta}").alias(f"Daily TBH_{theta}"),
                                F.avg(f"TBV_{theta}").alias(f"Daily TBV_{theta}"),).toPandas()

            # Display plot using Seaborn
            sns.lineplot(x='Date', y=f'Daily TBH_{theta}',
                        data=pdf, label=f'Daily TBH_{theta}')
            sns.lineplot(x='Date', y=f'Daily TBV_{theta}',
                        data=pdf, label=f'Daily TBV_{theta}')

        plt.xlabel('Date')
        plt.ylabel('Daily Average')
        plt.show()
