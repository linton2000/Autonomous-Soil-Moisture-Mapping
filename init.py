from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler(data_opt='tibobs')
    df = params.df_handler.data_df
    df.select('Avg_SM_LC').show(100)