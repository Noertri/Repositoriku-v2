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

t=hgtransform;
set(h,'Parent',t);
h=t;
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');
zlim([-6 6]);
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
