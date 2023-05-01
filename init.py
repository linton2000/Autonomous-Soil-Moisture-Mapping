from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler()
    params.load_tibetan_csv_data(csv1='ELBARA-III dataset-2016-2017ELBARA-III TB.csv',
                                 csv2='ELBARA-III dataset-2016-2017SMST_LC.csv',
                                 csv3='ELBARA-III dataset-2016-2017SMST_Z.csv')
    #params.print_data_df()