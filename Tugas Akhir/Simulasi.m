
t=0:0.001:10;

set1 = setfun(5,t);
set2 = setfun(0,t);
set3 = setfun(0,t);
set4 = setfun(0,t);

zout = gerak_z(set1,t);
[yout,phiout] = gerak_roll(set2,t);
[xout,thetaout] = gerak_pitch(set3,t);
yawout = gerak_yaw(set4,t);

data=struct('dat1',[xout,yout,zout],'dat2',[phiout,thetaout,yawout]);
% 
Visualisasi(data);