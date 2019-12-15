[X,Y] = meshgrid(1:34,1:34);
Z = ones(34);

Z = csvread('change.csv');
v=[0,0];
contour(X,Y,Z,v);
[xx, yy] = meshgrid(1:0.01:34);  %force it to interpolate at every 10th pixel
contourf(interp2(Z,xx,yy),[min(Z(:)); 0]);
colormap([1,0,0; 0,0,1]);
%greenColorMap = ones(1,256);
%redColorMap = ones(1,256);
%colorMap = [zeros(1, 256); zeros(1, 256); ones(1, 256)]';
%colormap(colorMap);
view(2);