import scipy.io as sp
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import pandas as pd

def load_mat_into_pd(fpath, matVar):
    mat = sp.loadmat('matlab_lmeb/geodata_r1.mat')  # load mat-file
    mdata = mat['fdata']  # variable in mat file
    mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
    # * SciPy reads in structures as structured NumPy arrays of dtype object
    # * The size of the array is the size of the structure array, not the number
    #   elements in any particular field. The shape defaults to 2-dimensional.
    # * For convenience make a dictionary of the data using the names from dtypes
    # * Since the structure has only one element, but is 2-D, index it at [0, 0]
    mdtype
    ndata = {n: mdata[n][0, 0] for n in mdtype.names}
    # Reconstruct the columns of the data table from just the time series
    # Use the number of intervals to test if a field is a column or metadata
    columns = [n for n, v in ndata.iteritems() if v.size == ndata['numIntervals']]
    # now make a data frame, setting the time stamps as the index
    df = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                    index=[datetime(*ts) for ts in ndata['timestamps']],
                    columns=columns)
    
def pretty_print_2d(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))