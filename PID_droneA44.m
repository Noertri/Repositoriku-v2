clear all
clf
%%%%%%%%%%%%%%%%%%%%%
% Property sistem
g = 9.81; m = 0.5; d = 0.25;
KF = 3.e-6; KM = 1.e-7;
KD = 0.25;
Ixx = 5.e-3; Iyy = Ixx; 
Izz = 10.e-3;
% Simpangan arah x
Ax = [0 1 ; 0 -KD/m];
Bx = [0 ; g];
Cx = [1 0]; Dx = 0;
[num, den] = ss2tf(Ax, Bx, Cx, Dx);
sysx = tf(num, den);
% Simpangan arah y
Ay = [0 1 ; 0 -KD/m];
By = [0 ; -g];
Cy = [1 0]; Dy = 0;
[num, den] = ss2tf(Ay, By, Cy, Dy);
sysy = tf(num, den);
% Simpangan arah z
Az = [0 1 ; 0 -KD/m];
Bz = [1 ; 1/m];
Cz = [1 0]; Dz = 0;
[num, den] = ss2tf(Az, Bz, Cz, Dz);
sysz = tf(num, den);
% % integrasi Euler
% x0 = [ 0 0]'; y0 = x0; z0 = x0;
% U = 1.;
% dt = 0.01;
% for i = 1:400
%     time(i) = (i-1)*dt;
%     U = 1; % 0.2;
%     xdot = Ax*x0 + Bx*U; x = x0 + xdot * dt;    x0 = x; xout = Cx*x;
%     ydot = Ay*y0 + By*U; y = y0 + ydot * dt;    y0 = y; yout = Cy*y; 
%     zdot = Az*z0 + Bz*U; z = z0 + zdot * dt;    z0 = z; zout = Cz*z;
%     x1(i) = xout;
%     y1(i) = yout;
%     z1(i) = zout;
% end
% % figure (1)
% % plot(time, x1); hold on; 
% % plot(time, y1,'color','red'); hold on;  plot(time, z1,'color','magenta'); 
% % grid on;
% 
% Sudut pitch
Ap = [0 1 ; 0 0];
Bp = [0 ; 1/Ixx];
Cp = [1 0]; Dp = 0;% 
[num, den] = ss2tf(Ap, Bp, Cp, Dp);
sysp = tf(num, den);
% Sudut roll
Ar = [0 1 ; 0 0];
Br = [0 ; 1/Iyy];
Cr = [1 0]; Dr = 0;% 
[num, den] = ss2tf(Ap, Bp, Cp, Dp);
sysr = tf(num, den);% 
% Sudut yaw
% Ayaw = [0 1 ; 0 0]; Byaw = [0 ; 1/Izz]; Cyaw = [1 0]; Dy = 0;% 
% [num, den] = ss2tf(Ayaw, Byaw, Cyaw, Dyaw);
% sysyaw = tf(num, den);
%%%%%%%%%%%%%%%
%%% Simpangan arah x
%%% sudut pitch dengan kontroler
Kpp = 0.0038; Ti = 24.69; Td = 6.173;
Kip = Kpp/Ti; Kdp = Kpp*Td;
numc = [Kdp Kpp Kip]; denc = [ 1 0 ]; % fungsi transfer controler PID pitch
Gcp = tf(numc, denc); % fungsi transfer controler PID pitch
sysp_seri1 = Gcp*sysp; % controler PID dan fungsi transfer sudut pitch
sysp_cl = feedback(sysp_seri1,1); % sistemm closed loop sudut pitch x
%%% simpangan x dengan kontroler
Kpx = 0.261; Ti = 5.305; Td = 1.326; % parameter f.transfer controler PID x
Kix = Kpx/Ti; Kdx = Kpx*Td; % fungsi transfer controler PID x
numc = [Kdx Kpx Kix]; denc = [ 1 0 ]; % fungsi transfer controler PID x
Gcx = tf(numc, denc); % fungsi transfer controler PID x
sysp_seri2 = Gcx*sysp_cl; % F.transfer yaw-PID dan dinamik simpangan x 
sysp_cl = feedback(sysp_seri2, sysx); % Sistem closed loop sudut pitch
%%% state space
numclp = sysp_cl.num{:}; denclp = sysp_cl.den{:};
[Ap1, Bp1, Cp1, Dp1] = tf2ss(numclp, denclp);
% %%% 
% sysx_seri3 = Gcx*sysp_cl*sysx; % F. transfer simpangan x
% sysx_cl = feedback(sysx_seri3,1);
%%%%
sysx_cl = feedback(sysx, sysp_seri2);
%%% state space
numclx = sysx_cl.num{:}; denclx = sysx_cl.den{:};
[Ax1, Bx1, Cx1, Dx1] = tf2ss(numclx, denclx);
%%%%%%%%%%%%%%%%%
%%% Simpangan arah y
%%% sudut roll dengan kontroler
Kpr = 0.0038; Ti = 24.69; Td = 6.173; % Gerak roll
Kir = Kpr/Ti; Kdr = Kpr*Td;
numc = [Kdr Kpr Kir]; denc = [ 1 0 ]; % fungsi transfer controler PID roll
Gcr = tf(numc, denc); % fungsi transfer controler PID roll
sysr_seri1 = Gcr*sysr; % controler PID dan fungsi transfer sudut roll
sysr_cl = feedback(sysr_seri1,1); % sistem closed loop roll
%%% simpangan y dengan kontroler
Kpy = -0.006; Ti = 2.067; Td = 0.517; % Gerak y
% Kpy = 0.261; Ti = 5.305; Td = 1.326; % parameter f.transfer controler PID y
Kiy = Kpy/Ti; Kdy = Kpy*Td; % fungsi transfer controler PID y
numc = [Kdy Kpy Kiy]; denc = [ 1 0 ]; % fungsi transfer controler PID y
Gcy = tf(numc, denc); % fungsi transfer controler PID y
sysr_seri2 = Gcy*sysr_cl; % F.transfer yaw-PID dan dinamik simpangan y 
sysr_cl = feedback(sysr_seri2, sysy); % Sistem closed loop sudut roll
%%% state space
numclr = sysr_cl.num{:}; denclr = sysr_cl.den{:};
[Ar1, Br1, Cr1, Dr1] = tf2ss(numclr, denclr);
%%%%%%%%%%%%
% sysy_seri3 = Gcy*sysr_cl*sysy;
% sysy_cl = feedback(sysy_seri3,1);
%%%
sysy_cl = feedback(sysy, sysr_seri2);
%%% state space
numcly = sysy_cl.num{:}; dencly = sysy_cl.den{:};
[Ay1, By1, Cy1, Dy1] = tf2ss(numcly, dencly);
%%%%
% % %%% Simpangan arah z
% Kpz = 1.86; Ti = 5.374; Td = 1.344; % Gerak z
Kpz = 2.86; Ti = 15.374; Td = 1.344; % Gerak z
Kiz = Kpz/Ti; Kdz = Kpz*Td;
numc = [Kdz Kpz Kiz]; denc = [ 1 0 ]; % fungsi transfer controler PID roll
Gcz = tf(numc, denc); % fungsi transfer controler PID roll
sysz_seri = Gcz*sysz; % controler PID dan fungsi transfer sudut roll
sysz_cl = feedback(sysz_seri,1); % sistemm closed loop roll
%%% state space
numclz = sysz_cl.num{:}; denclz = sysz_cl.den{:};
[Az1, Bz1, Cz1, Dz1] = tf2ss(numclz, denclz);
%%%%
% Sudut yaw
% state space sudut yaw
num = sysy.num{:}; den = sysy.den{:};
[Ayaw, Byaw, Cyaw, Dyaw] = tf2ss(num, den);
%sysy = tf(num, den);
%%%%
%%%%
% Skema integrasi euler 
p0 = zeros(6,1); r0 = zeros(6,1); % nilai awal sudut pitch dan roll
yaw0 = zeros(2,1); % nilai awal sudut yaw
Up = 0; Ur = 0; % U eksternal pitch dan roll % 
Uyaw = 0; % U eksternal yaw %
% Ux = 1; Uy = 1; Uz = 1; % U eksternal simpangan z
Ux = 0; Uy = 0; Uz = 0; % U eksternal simpangan z
% x0 = zeros(9,1); y0 = zeros(9,1); % nilai awal simpangan x dan y
x0 = zeros(6,1); y0 = zeros(6,1);
z0 = zeros(3,1); z0 = [20 0 0]'; % nilai awal simpangan z
%%%
dt = 0.01;
%%%
% [h thrusts] = quadcopter; % quadcopter animasi
h = Quadcopter; % quadcopter animasi
for i = 1:500 % 1601 % 1001 % 501 % 2000 % 401
    time(i) = (i-1)*dt;
    % Sudut pitch
    pdot = Ap1*p0 + Bp1*Up;
    p = p0 + pdot * dt;
    if ((i >= 50) && (i < 60))
        p(1) = p(1) + 0.25*rand(1,1);
    end
    p0 = p; 
    outp =  Cp1*p; 
    pitch(i) = outp;
    % Simpangan x dengan kontroler
%     % disturbance 
%     if ((i >= 100) && (i < 110))
%         outp = outp + + 10.*rand(1,1);
%     end    
    xdot = Ax1*x0 + Bx1*outp; % Ux;
    x = x0 + xdot * dt; 
    x0 = x; xout = Cx1 * x;
    simp_x(i) = xout;
    % Sudut roll
    rdot = Ar1*r0 + Br1*Ur;
    r = r0 + rdot * dt;
    if ((i >= 50) && (i < 60))
%        r(1) = r(1) + 0.05*rand(1,1);
        r(1) = r(1) + 0.25*rand(1,1);
    end
    r0 = r; 
    rout = Cr1*r;
    roll(i) = rout; % sudut roll
        % Simpangan y dengan kontroler
%     % disturbance
%     if ((i >= 100) && (i < 110))
%         rout = rout + 10.*rand(1,1);
%     end
    ydot = Ay1*y0 + By1*rout; % Uy;
    y = y0 + ydot * dt;
    y0 = y; yout = Cy1*y;
    simp_y(i) = yout;
%     % Simpangan z dengan kontroler
%     zdot = Az1*z0 + Bz1*Uz;
%     z = z0 + zdot * dt;
%     z0 = z; outz = Cz1*z;
%     simp_z(i) = outz;
%     %%%%
%     % sudut yaw
%     dyaw = Ayaw * yaw0 + Byaw*Uyaw;
%     yaw = yaw0 + dyaw * dt;
%     yaw0 = yaw; outyaw = Cyaw * yaw;
%     syaw(i) = outyaw;
    % sudut pitch, roll dan yaw. Sudut yaw = 0
    % pitch = x2(1); roll = y2(1); yaw = 0;
    % theta = [pitch(i) roll(i) syaw(i)]';
    theta = [pitch(i) roll(i) 0]';
    % altitude ?? x, y, dan z
    % posisi = [simp_x(i) simp_y(i) simp_z(i)]';
    posisi = [simp_x(i) simp_y(i) 20]';
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %   %%%% visualisasi
    dx = posisi; % x;
    move = makehgtform('translate',dx);
    % Compute rotation to correct angles. Then, turn this rotation
    % into a 4x4 matrix represting this affine transformation.
%     angles = deg2rad(theta);
%     rotate = rotation(angles);
%     rotate = [rotate zeros(3, 1);zeros(1, 3) 1];
    rotate = makehgtform('xrotate',theta(1,:),'yrotate',theta(2,:),'zrotate',theta(3,:));
    % Move the quadcopter to the right place, after putting 
    % it in the correct orientation.
    set(h,'Matrix', move*rotate); 
%     % Compute scaling for the thrust cylinders. The lengths should represent relative
%     % strength of the thrust at each propeller, and this is just a heuristic that seems
%     % to give a good visual indication of thrusts.
%     scales =exp(i/min(abs(i))+5)- exp(6)+1.5;
%     for is= 1:4
%     % Scale each cylinder. For negative scales, we need to flip the cylinder
%     % using a rotation, because makehgtform does not understand negative scaling.
%     % s = scales(is);
%         s = scales(is)/200.;
%         if s<0
%         scalez = makehgtform('yrotate',pi)*makehgtform('scale', [1, 1,abs(s)]);
%         elseif s>0
%         scalez = makehgtform('scale', [1, 1, s]);
%         end
%         % Scale the cylinder as appropriate, then move it to
%         % be at the same place as the quadcopter propeller.
%         set(thrusts(is),'Matrix', move*rotate*scalez);
%         %%%%%%
        view (45,60); % (45, 45);
%        view (135, 60);
%     end    
    %%%%
    pause(0.05); 
end
% figure (2)
% plot (time, pitch); hold on; 
% plot (time, roll);
% grid on;
% figure (3)
% plot (time, simp_x,'color','green'); hold on;
% plot (time, simp_y,'color','blue'); hold on;
% plot (time, simp_z,'color','red');
% grid on; 
