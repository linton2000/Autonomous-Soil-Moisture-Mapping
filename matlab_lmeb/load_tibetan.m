function [data_mtx] = load_tibetan
% Loads Tibetan study csv files into a table in matlab matrix format

meas_mtx = readmatrix('../TB_measurement_data.csv');
vald_mtx = readmatrix('../SM_temp_validation_data.csv');

disp(size(meas_mtx));
disp(size(vald_mtx));
data_mtx = 0;
end