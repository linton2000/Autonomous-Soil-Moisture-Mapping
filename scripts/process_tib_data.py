from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import sys

# Have to use sys.path for relative imports from a main script in sub_dir
ROOT_DIR = '/Users/lintoncharles/Documents/University/FIT4701_2/code/Autonomous-Soil-Moisture-Mapping/'
sys.path.append(ROOT_DIR)
from DataFrameHandler import DataFrameHandler

if __name__ == '__main__':
    df_handler = DataFrameHandler()
    df_handler.data_df = df_handler.data_df.dropna().drop('Datetime_LC').drop('Datetime_LAI')
    df_handler.print_data_df(show_all=True)
    df_handler.data_df.write.option("header",True)\
                            .option("delimiter","|")\
                            .csv("combined_tibobs")