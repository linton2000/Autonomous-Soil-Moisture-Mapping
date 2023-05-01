from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler()
    params.load_tibetan_csv_data(csv1='TB_measurement_data.csv',
                                 csv2='SM_temp_validation_data.csv')
    params.print_data_df()