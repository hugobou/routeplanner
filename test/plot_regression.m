function plot_regression(x, y)
  x(isnan(y)) = [] ;
  y(isnan(y)) = [] ;
  P = polyfit(x,y,1);
  %
  x0 = min(x) ; x1 = max(x) ;
  xi = linspace(x0,x1) ;
  yi = P(1)*xi+P(2);
  
  plot(x, y, '.')
  hold on
  plot(xi,yi,'r') ;
  hold off
end