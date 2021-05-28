clear all
a=[0 1;0 -(0.25/0.5)];
b=[0; -9.81];
c=[1 0];
d=0;

[num,den]=ss2tf(a,b,c,d);
ys=tf(num,den);

rolls=tf(200, [1 0 0]);
rolcl=feedback(rolls,1);

ycl=feedback(rolcl*ys,1);
phicl=feedback(rolcl,ys);

t=0:0.1:10;
u=setfun(0.5,t);

yout=lsim(ycl,u,t);
phiout=lsim(phicl,u,t);

l=length(yout);
xout=zeros(l,1);
zout=zeros(l,1);
% phiout=zeros(l,1);
thetaout=zeros(l,1);
yawout=zeros(l,1);

data=struct('dat1',[xout,yout,zout],'dat2',[phiout,thetaout,yawout]);