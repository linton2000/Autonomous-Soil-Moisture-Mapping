function [] = store_tibetan(ret_mtx)
% Stores to csv the tibetan study matrix loaded by load_tibetan()
% with retrieved SM values in it

headers = {'Tbvcol', 'Tbhcol', 'stemp', 'dtemp', 'lai', 'true_sm', 'ret_sm'};
csv_path = '../ret_tibobs.csv';

% Write headers to csv file
fid = fopen(csv_path, 'w');
fprintf(fid, '%s,', headers{1:end-1});
fprintf(fid, '%s\n', headers{end});
fclose(fid);

% Store matrix as csv data
writematrix(ret_mtx, csv_path, 'WriteMode', 'append');
end