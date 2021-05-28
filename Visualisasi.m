function Visualisasi(data)

figure;

t=Quadcopter;

xlim([-8 8]);
xlabel('X(m)');
ylim([-8 8]);
ylabel('Y(m)');
zlim([-5 15]);
zlabel('Z(m)');
animate(data,t);
end

function animate(data1,model)

% k = animatedline;
% x = data1.dat1(:,1);
% y = data1.dat1(:,2);
% z = data1.dat1(:,3);

    for i=1:length(data1.dat1)
        
        dmove=data1.dat1(i,:);
%         dmove=[0,yout,0];
        phi=data1.dat2(i,1);
        theta=data1.dat2(i,2);
        yaw=data1.dat2(i,3);
        move=makehgtform('translate',dmove);
        rotation=makehgtform('xrotate',phi,'yrotate',theta,'zrotate',yaw);
        
        set(model,'Matrix',move*rotation);
%         addpoints(k,x(i),y(i),z(i));
%         comet3(k,x(i),y(i),z(i));
        pause(0.01);
    end
end

function h=Quadcopter()
h(1)=prism(-5,-0.25,-0.25,10,0.5,0.5);
h(2)=prism(-0.25,-5,-0.25,0.5,10,0.5);

[x, y, z]=sphere;
x=0.5*x;
y=0.5*y;
z=0.5*z;
h(3)=surf(x-5,y,z,'EdgeColor','none','FaceColor','b');
h(4)=surf(x+5,y,z,'EdgeColor','none','FaceColor','b');
h(5)=surf(x,y-5,z,'EdgeColor','none','FaceColor','b');
h(6)=surf(x,y+5,z,'EdgeColor','none','FaceColor','b');

%Draw thrust cylinders.
[x,y,z] = cylinder(0.1, 7);
h(7) = surf(x, y + 5, z,'EdgeColor','none','FaceColor','m');
h(8) = surf(x + 5, y, z,'EdgeColor','none','FaceColor','y');
h(9) = surf(x, y - 5, z,'EdgeColor','none','FaceColor','m');
h(10) = surf(x - 5, y, z,'EdgeColor','none','FaceColor','y');

t=hgtransform;
set(h,'Parent',t);
h=t;
grid on;
end

function h=prism(x, y, z, w, l, h)
[X, Y, Z]=prism_faces(x, y, z, w, l, h);

faces(1,:)=[4 2 1 3];
faces(2,:)=[4 2 1 3]+4;
faces(3,:)=[4 2 6 8];
faces(4,:)=[4 2 6 8]-1;
faces(5,:)=[1 2 6 5];
faces(6,:)=[1 2 6 5]+2;

for i = 1:size(faces,1)
    h(i)=fill3(X(faces(i,:)), Y(faces(i,:)), Z(faces(i,:)), 'r');
    hold on;
end

t=hgtransform;
set(h,'Parent',t);
h=t;
end

function [X, Y, Z]=prism_faces(x, y, z, w, l, h)
X=[x x x x x+w x+w x+w x+w];
Y=[y y y+l y+l y y y+l y+l];
Z=[z z+h z z+h z z+h z z+h];
end
