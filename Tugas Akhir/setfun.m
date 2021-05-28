function funcstep = setfun(u,t)
for i=1:length(t)
    if t(i)<=0
        funcstep(i)= 0;
    else
        funcstep(i)= u;
    end
end
