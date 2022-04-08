function [ax,ay,az]=rotateoverx(x,y,z)

phi=(-21)*pi/180;
v=[x;y;z];

a=[1 0 0; 0 cos(phi) sin(phi); 0 -sin(phi) cos(phi)];

r=a*v;
ax=r(1)
ay=r(2)
az=r(3)
