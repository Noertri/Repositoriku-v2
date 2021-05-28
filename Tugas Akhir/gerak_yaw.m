function yawout = gerak_yaw(u,t)
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
Ayw=[0,1;0,0];
Byw=[0;1/Izz];
Cyw=[1,0];
Dyw=0;

%Fungsi transfer gerak roll
[numyw,denyw]=ss2tf(Ayw,Byw,Cyw,Dyw);
yaws=tf(numyw,denyw);

% Parameter pengendali gerak roll
Kpyw=7.5e-3;
Tiyw=24.69;
Tdyw=6.173;
Kiyw=Kpyw/Tiyw;
Kdyw=Kpyw*Tdyw;
yawc=tf([Kdyw,Kpyw,Kiyw],[0,1,0]);

% Fungsi transfer closed-loop
yawcl=feedback(yaws*yawc,1);

yawout=lsim(yawcl,u,t);

% Respon fungsi tangga
% step(yawcl,0:0.1:10)
% grid on
% hold on
end