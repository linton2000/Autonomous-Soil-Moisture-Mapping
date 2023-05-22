from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler(data_opt='tibetan')
    params.df_handler.print_data_df(show_all=True)
    params.df_handler.plot_TB_time()
    #params.df_handler.plot_SM_TB()