function zout = gerak_z(u, t)
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

% State-space gerak pada sumbu z
Az=[0,1;0,-Kd/m];
Bz=[0;1/m];
Cz=[1,0];
Dz=0;

% Fungsi transfer gerak pada sumbu z
[numz,denz]=ss2tf(Az,Bz,Cz,Dz);
zs=tf(numz,denz);

% Parameter pengendali gerak pada sumbu z
Kpz=1.86;
Tiz=5.374;
Tdz=1.344;
Kiz=Kpz/Tiz;
Kdz=Kpz*Tdz;
zc=tf([Kdz,Kpz,Kiz],[0,1,0]);

% Fungsi transfer closed-loop
zcl=feedback(zs*zc,1);

zout=lsim(zcl,u,t);

% Respon fungsi tangga
% step(zcl,0:0.1:10)
% grid on
% hold on
end