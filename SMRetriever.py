import csv
from MLRegressor import MLRegressor
from ParamHandler import ParamHandler


class SMRetriever:

    def __init__(self, params: ParamHandler) -> None:
        self.params: ParamHandler = params
        self.feats = ['TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', 'TBH_55', 'TBV_55', 'TBH_60',
                      'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70', 'LAI_hants', 'Avg_STS_LC', 'Avg_STD_LC']

    def save_basic_ml(self, type='no_temp', total_recs=3000, verbose=False):
        if type == 'no_temp':
            regressor = MLRegressor(self.feats[:-2])
        data_df = self.params.df_handler.data_df
        ml_df = data_df.sample(total_recs/data_df.count(), 42)
        res = []
        for n_recs in range(30, 2000, 10):
            print(f'Training model for n_recs = {n_recs}... Please Wait...', end='\r')
            train_ratio = n_recs/ml_df.count()
            evals = regressor.fit(
                df=ml_df, split=[train_ratio, 1-train_ratio], verbose=verbose)
            rec_dict = {'n_recs': n_recs, 'evals': evals}
            res.append(SMRetriever._flatten_dict(rec_dict))

        with open("basic_ml.csv", "w") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=res[0].keys())
            writer.writeheader()
            for row in res:
                writer.writerow(row)

    def _flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(SMRetriever._flatten_dict(
                    v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
