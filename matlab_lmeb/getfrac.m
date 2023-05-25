function [fractions,fflag,cloud]=getfrac(y,x,pixel)
global woodland bares LANDCOVER30m
%Get fraction covers of all vegetation types within each PLMR pixel
% from the 30m Landsat derived landcover map (Boulet)
% NOTE: open woodland fraction is assimilated into other classes
% according to parameter "woodland" which references Boulet's vegetation
% codes

% flag==1 is returned when the sum of fractions is not 100%(due to either
% partial cloud cover or other problems)

% cloud==1 is returned whenever any percentage of pixel is covered by
% cloud, or cloud shadow


%calculate geographical area covered by pixel
y1=y+0.5*pixel;
y2=y-0.5*pixel;
x1=x-0.5*pixel;
x2=x+0.5*pixel;

% extract subset of LANDCOVER map (30m) within pixel
 [row1, col1]=latlon2pix(LANDCOVER30m.R,y1,x1);
 [row2, col2]=latlon2pix(LANDCOVER30m.R,y2,x2);
 row1=uint16(row1);
 row2=uint16(row2);
 col1=uint16(col1);
 col2=uint16(col2);
 
 subset=LANDCOVER30m.A(row1:row2,col1:col2);


% convert evantual woodland and/or bare fraction to either grassland or forest
if ~isempty(subset(subset==1))
subset(subset==1)=woodland;
end
if ~isempty(subset(subset==5))
subset(subset==5)=bares;
end
if ~isempty(subset(subset==12))
subset(subset==12)=bares;
end

% calculate fractions within subset
n=numel(subset(~isnan(subset))); %total,non NaN element


bare=[5 12];  % Boulet's vegetation codes
grass=[4 6 7];
crop=[8 9 13];
forest=[2 3];
cloud=[10 11];

bare_frac=numel(subset(subset==bare(1) | subset==bare(2)))/n;
grass_frac=numel(subset(subset==grass(1) | subset==grass(2) | subset==grass(3)))/n;
crop_frac=numel(subset(subset==crop(1) | subset==crop(2) | subset==crop(3)))/n;
forest_frac=numel(subset(subset==forest(1) | subset==forest(2)))/n;

%Assemble outputs
fractions=[bare_frac grass_frac crop_frac forest_frac];
cloud=numel(subset(subset==cloud(1) | subset==cloud(2)))/n; 

% return lways fflag==0 --> retrieval done for all pixels
fflag=0;
%flag cloud-covered pixels
% if sum(fractions)>0.5
%     fflag=1;
% else
%     fflag=0;
% end    
    
    






