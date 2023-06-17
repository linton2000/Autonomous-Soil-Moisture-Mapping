from SMRetriever import SMRetriever
from ParamHandler import ParamHandler

if __name__ == '__main__':
    params = ParamHandler(data_opt='tibobs')
    retriever = SMRetriever(params=params)
    retriever.save_basic_ml()