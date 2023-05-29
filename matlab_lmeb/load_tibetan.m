function [Tbvcol, Tbhcol, stemp, dtemp, lai, true_sm] = load_tibetan(nrecs)
% Loads nrecs rows from Tibetan csv file into matrix 
% and returns it along with 40 degs TBh & Tbv, surface temp, 
% ground temp (5cm+) and MODIS LAI data as ordered column vectors

tib_mtx = readmatrix('../combined_tibobs.csv');
tib_mtx = tib_mtx(1:nrecs, :);

Tbvcol = tib_mtx(:, 2);
Tbhcol = tib_mtx(:, 3);
true_sm = tib_mtx(:, 16);
stemp = tib_mtx(:, 17);
dtemp = tib_mtx(:, 18);
lai = tib_mtx(:, 19);
end