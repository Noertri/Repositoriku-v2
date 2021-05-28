function [yout, phiout] = gerak_roll(u,t)
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

%State-space gerak roll
Ar=[0,1;0,0];
Br=[0;1/Ixx];
Cr=[1,0];
Dr=0;

%Fungsi transfer gerak roll
[numr,denr]=ss2tf(Ar,Br,Cr,Dr);
rolls=tf(numr,denr);

% Parameter pengendali gerak roll
Kpr=3.8e-3;
Tir=24.69;
Tdr=6.173;
Kir=Kpr/Tir;
Kdr=Kpr*Tdr;
rc=tf([Kdr,Kpr,Kir],[0,1,0]);

% Fungsi transfer closed-loop
rcl=feedback(rolls*rc,1);

% State-space gerak y
Ay1=[0,1;0,-Kd/m];
By1=[0;g];
Cy1=[1,0];
Dy1=0;

% Fungsi transfer gerak pada sumbu y
[numy1,deny1]=ss2tf(Ay1,By1,Cy1,Dy1);
y1s=tf(numy1,deny1);

% Parameter pengendali gerak pada sumbu y
Kpy=0.261;
Tiy=5.305;
Tdy=1.326;
Kiy=(Kpy/Tiy);
Kdy=Kpy*Tdy;
ycs=tf([Kdy,Kpy,Kiy],[0,1,0]);

% Fungsi transfer closed-loop 1
y1cl=feedback((rcl*ycs),y1s);

% Fungsi transfer closed-loop 2
y2cl=feedback(ycs*rcl*y1s,1);

yout=lsim(y2cl,u,t);
phiout=lsim(y1cl,u,t);

% Respon fungsi tangga
% figure(1)
% step(rcl,0:0.1:10)
% grid on
% hold on
% figure(2)
% step(y2cl,0:0.1:20)
% grid on
% hold on

end