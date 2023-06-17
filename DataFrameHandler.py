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
            pd.set_option('display.max_columns', None)
            print('\nStatistical Summary:')
            print(self.data_df.toPandas().describe())