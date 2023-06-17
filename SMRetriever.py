import csv
import pandas as pd
import matplotlib.pyplot as plt
from MLRegressor import MLRegressor
from ParamHandler import ParamHandler


class SMRetriever:

    def __init__(self, params: ParamHandler) -> None:
        self.params: ParamHandler = params
        self.feats = ['TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', 'TBH_55', 'TBV_55', 'TBH_60',
                      'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70', 'LAI_hants', 'Avg_STS_LC', 'Avg_STD_LC']
    
    def plot_basic_ml(self, file_path='basic_ml.csv'):
        df = pd.read_csv(file_path)
        _, axs = plt.subplots(2, 2, figsize=(10, 10))

        axs[0, 0].plot(df['n_recs'], df['evals_Linear Regression_rmse'], label='RMSE')
        axs[0, 0].plot(df['n_recs'], df['evals_Linear Regression_mae'], label='MAE')
        axs[0, 0].plot(df['n_recs'], df['evals_Linear Regression_r2'], label='R2')
        axs[0, 0].set_title('Linear Regression')
        axs[0, 0].legend()

        axs[0, 1].plot(df['n_recs'], df['evals_Decision Tree_rmse'], label='RMSE')
        axs[0, 1].plot(df['n_recs'], df['evals_Decision Tree_mae'], label='MAE')
        axs[0, 1].plot(df['n_recs'], df['evals_Decision Tree_r2'], label='R2')
        axs[0, 1].set_title('Decision Tree')
        axs[0, 1].legend()

        axs[1, 0].plot(df['n_recs'], df['evals_Random Forest_rmse'], label='RMSE')
        axs[1, 0].plot(df['n_recs'], df['evals_Random Forest_mae'], label='MAE')
        axs[1, 0].plot(df['n_recs'], df['evals_Random Forest_r2'], label='R2')
        axs[1, 0].set_title('Random Forest')
        axs[1, 0].legend()

        axs[1, 1].plot(df['n_recs'], df['evals_Gradient Boosted Tree_rmse'], label='RMSE')
        axs[1, 1].plot(df['n_recs'], df['evals_Gradient Boosted Tree_mae'], label='MAE')
        axs[1, 1].plot(df['n_recs'], df['evals_Gradient Boosted Tree_r2'], label='R2')
        axs[1, 1].set_title('Gradient Boosted Tree')
        axs[1, 1].legend()

        plt.show()
    
    def plot_basic_rmse(self, file_path='basic_ml.csv'):
        df = pd.read_csv(file_path)
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        ax.plot(df['n_recs'], df['evals_Decision Tree_rmse'], label='Decision Tree')
        ax.plot(df['n_recs'], df['evals_Random Forest_rmse'], label='Random Forest')
        ax.plot(df['n_recs'], df['evals_Gradient Boosted Tree_rmse'], label='Gradient Boosted Tree')

        ax.set_title('RMSE vs. No. of Training Records')
        ax.set_xlabel('No. of Training Records')
        ax.set_ylabel('RMSE')

        plt.legend()
        plt.show()
    
    def plot_angle_gbt(self, split=[0.7, 0.3], total_recs=10000, metric='rmse', angle_dict=None):
        data_df = self.params.df_handler.data_df
        ml_df = data_df.sample(total_recs/data_df.count(), 42)
        if angle_dict == None:
            angle_dict = {'40': 0, '45': 0, '50': 0, '55': 0, '60': 0, '65': 0, '70': 0}
        for angle in angle_dict.keys():
            feats = [f'TBH_{angle}', f'TBV_{angle}', f'LAI_hants']
            regressor = MLRegressor(feats)
            eval = regressor.fit(metric=metric, df=ml_df, split=split, type='feat')
            angle_dict[angle] = eval
        _, ax = plt.subplots()
        ax.bar(angle_dict.keys(), angle_dict.values())
        ax.set_title(f'Gradient Boosted Tree RMSE for each incidence angle')
        ax.set_xlabel('Incidence Angle')
        ax.set_ylabel(f'RMSE (Root Mean Squared Error)')
        plt.show()
    
    def plot_pol_gbt(self, split=[0.7, 0.3], total_recs=5000, metric='rmse'):
        data_df = self.params.df_handler.data_df
        ml_df = data_df.sample(total_recs/data_df.count(), 42)
        pol_dict = {'V-pol': 0, 'H-pol': 0}
        for pol in pol_dict.keys():
            feats = [feat for feat in self.feats if feat[2] == pol[0]]
            regressor = MLRegressor(feats)
            eval = regressor.fit(metric=metric, df=ml_df, split=split, type='feat')
            pol_dict[pol] = eval
        print(pol_dict)
        _, ax = plt.subplots()
        ax.bar(pol_dict.keys(), pol_dict.values())
        ax.set_title(f'Gradient Boosted Tree RMSE for each polarisation')
        ax.set_xlabel('Polarisation')
        ax.set_ylabel(f'RMSE (Root Mean Squared Error)')
        plt.show()

    def plot_feat_imports(self, split=[0.7, 0.3], total_recs=5000):
        data_df = self.params.df_handler.data_df
        ml_df = data_df.sample(total_recs/data_df.count(), 42)
        regressor = MLRegressor(self.feats[:-3])
        importances, feats = regressor.fit(df=ml_df, split=split, type='dt')
        _, ax = plt.subplots()
        ax.bar(feats, importances)
        ax.set_title('Feature Importances of Decision Tree Regressor')
        ax.set_xlabel('Feature Name')
        ax.set_ylabel('Importance')
        plt.show()

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
