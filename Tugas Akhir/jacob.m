clc;
clear all;

syms x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12
syms u1 u2 u3 u4
syms m g Kd Ixx Iyy Izz s

% Parameter 
m=0.5;
g=9.81;
Kd=0.25;
Ixx=0.005;
Iyy=0.005;
Izz=0.01;

x1dot=x2;
x2dot=u1*(1/m)*(cos(x11)*sin(x9)*cos(x7)-sin(x7)*sin(x11))-(Kd/m)*x2;
x3dot=x4;
x4dot=u1*(1/m)*(cos(x7)*sin(x9)*sin(x11)+sin(x7)*cos(x11))-(Kd/m)*x4;
x5dot=x6;
x6dot=u1*(1/m)*(cos(x7)*cos(x9))-(Kd/m)*x6;
x7dot=x8;
x8dot=x10*x12*((Iyy-Izz)/Ixx)+u2*(1/Ixx);
x9dot=x10;
x10dot=x8*x12*((Izz-Ixx)/Iyy)+u3*(1/Iyy);
x11dot=x12;
x12dot=x8*x10*((Ixx-Iyy)/Izz)+u4*(1/Izz);

% Linearisasi
a(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,u1) = jacobian([x1dot,x2dot,x3dot,x4dot,x5dot,x6dot,x7dot,x8dot,x9dot,x10dot,x11dot,x12dot],[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12]);
b(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12) = jacobian([x1dot,x2dot,x3dot,x4dot,x5dot,x6dot,x7dot,x8dot,x9dot,x10dot,x11dot,x12dot],[u1,u2,u3,u4]);

% Subtitusi titik equilibrium
digits(3);
A = vpa(a(0,0,0,0,0,0,0,0,0,0,0,0,m*g));
B = vpa(b(0,0,0,0,0,0,0,0,0,0,0,0));
C = eye(12,12);
D = zeros(12,4);
I = eye(12,12);

a2(x2,x7,x9,x11,u1)=jacobian([x1dot,x2dot],[x1,x2,x7,x9,x11,u1]);
a4(x4,x7,x9,x11,u1)=jacobian([x3dot,x4dot],[x3,x4,x7,x9,x11,u1]);
a6(x6,x7,x9,x11,u1)=jacobian([x5dot,x6dot],[x5,x6,x7,x9,x11,u1]);
a8(x10,x12,u2)=jacobian([x7dot,x8dot],[x7,x8,x10,x12,u2]);
a10(x8,x12,u3)=jacobian([x9dot,x10dot],[x9,x10,x8,x12,u3]);
a12(x8,x10,u4)=jacobian([x11dot,x12dot],[x11,x12,x8,x10,u4]);

digits(3);
A2 = vpa(a2(0,0,0,0,m*g));
A4 = vpa(a4(0,0,0,0,m*g));
A6 = vpa(a6(0,0,0,0,m*g));
A8 = vpa(a8(0,0,0));
A10 = vpa(a10(0,0,0));
A12 = vpa(a12(0,0,0));

% digits(4);
G = C*(inv(s*I-A))*B + D;
% pretty(Gs);