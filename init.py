from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler(data_opt='tibetan')
    params.df_handler.print_data_df(show_table=True, show_schm=True)