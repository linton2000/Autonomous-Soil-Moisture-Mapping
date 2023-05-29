function rmse = compute_rmse(x, y)
    n = length(x);
    rmse = sqrt(sum((x - y).^2) / n);
end