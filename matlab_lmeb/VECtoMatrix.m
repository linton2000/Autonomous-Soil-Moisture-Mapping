SM{1}=NaN*ones(46,51);
SM{2}=NaN*ones(46,51);
SM{3}=NaN*ones(46,51);
for k=1:3
    m=1;
    for i=5:46
        for j=6:42
            XA_matrix{k}(j,i)=XA{k}(m);
            m=m+1;
        end
    end
end
    