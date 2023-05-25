function z=compfilt(x,y)

if (~isempty(y))
fic=(x==y(1));
lgy=length(y);

for i=1:lgy,
fi=(x==y(i));
fic=fic|fi;
end

z=filt(fic);
end


