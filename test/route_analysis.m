data=dlmread("analysis.csv");

data2=dlmread("analysis_invalids.csv");
no_route_idx = data2(:,7) < 0;
no_route = data2(no_route_idx, :)(:, [1 4]);


for i = 1:length(no_route)
  src = no_route(i, 1); dst = no_route(i, 2);
  data((data(:,1)==src)&(data(:,4)==dst), :) = [];
endfor


l_dijk_invalid = data2(data2(:,7) > 0, :)(:,7);



valid = data(:,8) >= 0;
n_valid = sum(valid == 1);
n_invalid = sum(valid == 0);

data_valid = data(valid, :);
l_dijk = data_valid(:,7);
l_calc = data_valid(:,8);
l_ratio =  l_calc ./ l_dijk;

plot(l_dijk, l_ratio, '.')
##pause
plot(l_dijk, l_calc, '.')
##pause


labels_ratio = ['[0,2)';'[2,4)';'[4,6)';'[6,8)';'[8,10)';'[10,20)';'[10,100)'];
hist_bins_ratio = [0,2,4,6,8,10,20,100];
hist_ratio = histc(l_ratio, hist_bins_ratio)(1:end-1) ./ n_valid;
bar(hist_ratio)
set(gca, "fontsize", 16)
set(gca, 'XTickLabel', labels_ratio);  

plot(1, l_dijk, '.b')
hold on
plot(2, l_dijk_invalid, '.r')