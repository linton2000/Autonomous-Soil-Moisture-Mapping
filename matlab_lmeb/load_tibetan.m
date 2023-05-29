%function [] = load_tibetan
% Loads Tibetan study csv files into a table in matlab matrix format

tib_mtx = readmatrix('../combined_tibobs.csv');

disp(size(tib_mtx));
%end