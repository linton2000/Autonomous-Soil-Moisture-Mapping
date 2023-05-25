% function mcov=corr_function(mat)
% mcov=corr_function(mat,h1,h2) where mat is the matrix of which you want to
% extract the correlation fonction;
% mcov is the correlation function matrix;
% mcov(i,j) correpond to to the correlation coeff of h(i-1,j-1) where i is
% horizontaly and j verticaly.
mat=X;

if size(mat)>40
    sz=[40,40]
else
    sz=size(mat);
    
end
h1=4
h2=4

mcov=zeros(h1-1,h2-1);
% i and j represents the translation h(i,j) 
% starting h is h(0,0) and maximum is defined as 40
% mcov(i,j)=corr(h(i-1,j-1)); which means that when i=j=1
% mcov(1,1)=cor(h(0,0))
for i=0:(h1-1)
    for j=0:(h2-1)
        trans=zeros(size(mat));
        trans(1:size(mat,1)-i,1:size(mat,2)-j)=mat(i+1:end,j+1:end);
        ori=mat(1:size(mat,1)-i,1:size(mat,2)-j);
        moved=trans(1:size(mat,1)-i,1:size(mat,2)-j);
        coeff=corrcoef(double(ori(:)),double(moved(:)));
        if size(coeff,1)==1
            mcov(h1+2-i,h2+2-j)=1;
        else
            mcov(i+1,j+1)=coeff(1,2);
        end
    end
end


mcov2=zeros(2*h1-1,2*h2-1);
for i=1:(h1)
    for j=1:(h2)
        if i==1 & j==1
            mcov2(h1,h2)=mcov(i,j);
        else
            mcov2(h1+1-i,h2+1-j)=mcov(i,j);
            mcov2(h1+1-i,h2-1+j)=mcov(i,j);
            mcov2(h1-1+i,h2+1-j)=mcov(i,j);
            mcov2(h1-1+i,h2-1+j)=mcov(i,j);
        end
    end
end
h1_d=-h1-1:1:h1+1;
h2_d=-h2-1:1:h2+1;
mesh(h1_d,h2_d,mcov2)
