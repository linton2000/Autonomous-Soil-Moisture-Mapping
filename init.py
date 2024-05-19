import scipy.io
mat_data = scipy.io.loadmat('matlab_lmeb/geodata_r1.mat')
print(mat_data['fdata'])