import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('ret_tibobs.csv')
    true_sm = [round(i, 3) for i in df['true_sm']]
    ret_sm = [round(i, 3) for i in df['ret_sm']]
    plt.plot(true_sm, ret_sm)
    plt.xlabel('Profile Soil Moisture (V/V)')
    plt.ylabel('Retrieved Soil Moisture (V/V)')
    plt.title('Error in L-MEB Soil Moisture Retrieval')
    plt.show()