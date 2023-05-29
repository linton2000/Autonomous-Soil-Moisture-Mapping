import matplotlib.pyplot as plt
import numpy as np
# Relative imports from root directory
import sys
ROOT_DIR = '/Users/lintoncharles/Documents/University/FIT4701_2/code/Autonomous-Soil-Moisture-Mapping/'
sys.path.append(ROOT_DIR)
from MLRegressor import MLRegressor
from ParamHandler import ParamHandler

if __name__ == '__main__':
    nrecs = 1000
    params = ParamHandler(data_opt='tibobs')
    regressor = MLRegressor(params, numRecs=nrecs, without_temp=True)
    splits = [[round(i, 2), round(1-i, 2)] for i in np.arange(start=0.01, stop=0.30, step=0.02)]
    rmse_arr = np.zeros(len(splits))
    for algo in ['Linear', 'Decision Tree', 'Random Forest']:
        for i in range(len(splits)):
            rmse_arr[i] = regressor.fit(type=algo, split=splits[i])
        x_splits = [round(i*100, 2) for i, _ in splits]
        plt.scatter(x_splits, rmse_arr, label={algo + ' Regression'}, marker='x')
    plt.xlabel('Training Data Split (%)')
    plt.ylabel('Root Mean Squared Error')
    plt.title(f'Generalisability of ML models (for {nrecs} samples)')
    plt.legend()
    plt.show()