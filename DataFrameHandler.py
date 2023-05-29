from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY


class DataFrameHandler():
    def __init__(self, data_opt) -> None:
        # Spark Initalisation
        root_dir = '/Users/lintoncharles/Documents/University/FIT4701_2/code/Autonomous-Soil-Moisture-Mapping/'
        spark = SparkSession.builder\
                            .master('local[*]')\
                            .appName('SM Retreival App')\
                            .config('spark.sql.warehouse.dir', root_dir)\
                            .getOrCreate()
        spark.sparkContext.setLogLevel('ERROR')

        # Loading CSV Data
        csv_path = ''
        if data_opt == 'tibobs': csv_path = 'combined_tibobs.csv'
        self.data_df = spark.read.format('csv')\
                                 .options(header=True, multiline=True, inferSchema=True)\
                                 .option('delimiter', '|')\
                                 .load(csv_path)

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
    def plot_TB_time(self, min_date='2016-09-01', max_date='2016-12-01', TB_angles=[40, 45]):
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

    def plot_SM_TB(self, TB_angles=[40, 45]):
        cols = [('Surface Temp', 'Avg_STS_LC')]
        for theta in TB_angles:
            for P in ['H', 'V']:
                cols.append((f'TB{P}_{theta}', f'TB{P}_{theta}'))
        # Grouping columns by rounded SM and average TB/Temp values for each group
        for labl, col in cols:
            pdf = self.data_df.groupBy(F.round(F.col('Avg_SM_LC'), 3).alias('True SM'))\
                .agg(F.avg(F.col(col)).alias(labl)).toPandas()
            sns.lineplot(x=labl, y='True SM',
                         data=pdf, label=labl)

        plt.xlabel('TB & Surface Temp (Kelvin)')
        plt.ylabel('Soil Moisture (v/v)')
        plt.show()
