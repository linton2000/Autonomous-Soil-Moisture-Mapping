function  [sand,clay,rob]=getsoil(y,x,pixel)
global CLAY BULK MalvernClay MalvernSand


% extract subset of soil texture maps (1km) within PLMR pixel
%  [row, col]=latlon2pix(CLAY.R,y,x);
  [row, col]=latlon2pix(MalvernClay.R,y,x);
% clay=CLAY.A(uint16(row),uint16(col));
%  sand=SAND.A(uint16(row),uint16(col)); 
clay=MalvernClay.A(uint16(row),uint16(col));
sand=MalvernSand.A(uint16(row),uint16(col));

clear row col
 [row, col]=latlon2pix(CLAY.R,y,x);
 rob=BULK.A(uint16(row),uint16(col)); % maps have same georeference, therefore
                                           % row1, row2, col1 and col2 are
                                           % the same



    






