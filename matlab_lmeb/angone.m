function lig=angone(x)
% selec le premier numero de lig , pour chaq elmt du vect x

y=x;

i=0;
while (~isempty(y)),
i=i+1;

fi=(x==y(1));
ligxy=filt(fi);
lig(i)=ligxy(1);

fi=(y==y(1));
ligxy=filt(fi);
y(ligxy)=[];

end





