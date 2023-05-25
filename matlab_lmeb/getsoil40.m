% Modified from 'getsoil' in order to account
% for larger then 1km area

function  [sand,clay,rob]=getsoil(y,x,pixel)
global CLAY MalvernClay MalvernSand

%calculate geographical area covered by pixel
y1=y+0.5*pixel;
y2=y-0.5*pixel;
x1=x-0.5*pixel;
x2=x+0.5*pixel;

% extract subset of Lsoil texture maps (1km) within  pixel
 [row1, col1]=latlon2pix(MalvernClay.R,y1,x1);
 [row2, col2]=latlon2pix(MalvernClay.R,y2,x2);
 row1=uint16(row1);
 row2=uint16(row2);
 col1=uint16(col1);
 col2=uint16(col2);
 
subset_clay=MalvernClay.A(row1:row2,col1:col2);
subset_sand=MalvernSand.A(row1:row2,col1:col2);


clay=mean(subset_clay(~isnan(subset_clay)));
sand=mean(subset_sand(~isnan(subset_sand)));

rob=1.1;

% clear row col
%  [row, col]=latlon2pix(CLAY.R,y,x);
%  rob=BULK.A(uint16(row),uint16(col)); % maps have same georeference, therefore
%                                            % row1, row2, col1 and col2 are
%                                            % the same



    






