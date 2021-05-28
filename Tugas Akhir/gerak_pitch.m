function [xout,thetaout] = gerak_pitch(u,t)
% Property system
g=9.81;
m=0.5;
d=0.25;
Kf=3e-6;
Km=1e-7;
Kd=0.25;
Ixx=5e-3;
Iyy=5e-3;
Izz=10e-3;

%State-space gerak pitch
Ap=[0,1;0,0];
Bp=[0;1/Iyy];
Cp=[1,0];
Dp=0;

%Fungsi transfer gerak pitch
[nump,denp]=ss2tf(Ap,Bp,Cp,Dp);
pitchs=tf(nump,denp);

% Parameter pengendali gerak pitch
Kpp=3.8e-3;
Tip=24.69;
Tdp=6.173;
Kip=Kpp/Tip;
Kdp=Kpp*Tdp;
pic=tf([Kdp,Kpp,Kip],[0,1,0]);

% Fungsi transfer closed-loop
pitchcl=feedback(pitchs*pic,1);

% State-space gerak X
Ax1=[0,1;0,-Kd/m];
Bx1=[0;g];
Cx1=[1,0];
Dx1=0;

% Fungsi transfer gerak x
[numx1,denx1]=ss2tf(Ax1,Bx1,Cx1,Dx1);
x1s=tf(numx1,denx1);

% Parameter pengendali gerak pada sumbu x
Kpx=0.261;
Tix=5.305;
Tdx=1.326;
Kix=Kpx/Tix;
Kdx=Kpx*Tdx;
xcs=tf([Kdx,Kpx,Kix],[0,1,0]);

% Fungsi transfer closed-loop 1
x1cl=feedback((pitchcl*xcs),x1s);

% Fungsi transfer closed-loop 2
x2cl=feedback((xcs*pitchcl*x1s),1);

xout=lsim(x2cl,u,t);
thetaout=lsim(x1cl,u,t);

% Respon fungsi tangga
% figure(1)
% step(pitchcl,0:0.1:10)
% grid on
% hold on
% figure(2)
% step(x2cl,0:0.1:10)
% grid on
% hold on

end