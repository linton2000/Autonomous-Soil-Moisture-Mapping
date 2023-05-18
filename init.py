from LMEBRegressor import LMEBRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler(data_opt='tibetan')
    print(LMEBRegressor(params).fit())