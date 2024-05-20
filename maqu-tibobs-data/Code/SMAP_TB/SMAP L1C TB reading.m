% SMAP L1C TB reading
%
% Attention: This is for L1C SMAP brightness temperature, not L1B.
%
% Input: the path of SMAP .h5 format data (address)
% Anyone can register and download it from https://earthdata.nasa.gov/
%
% Output: UTC time  (dset Column 1)
%         tb_h_fore (dset Column 2)
%         tb_v_fore (dset Column 3)      
%         tb_h_aft  (dset Column 4)
%         tb_v_aft  (dset Column 5)
%         fc_lon: longitude of footprint center
%         fc_lon: latitude of footprint center
% 
% Copyright: Shaoning LV , Postdoc
% Meteorology Institute of University Bonn
%
% 05-03-2020
% e-mail: slvv@uni-bonn.de
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% retrieve SMAP TB 

% the path of SMAP .h5 format data
address     = 'C:\Users\Administrator\Downloads\SMAP_L1c_Maqu';
namelist    = ls([address '\SMAP_L1C_*.h5']);

lat_ELBARA  =  33.90;
lon_ELBARA  = 102.15;

% 25: tb_3_aft
% 26: tb_3_fore
% 27: tb_4_aft
% 28: tb_4_fore
% 37: tb_h_aft
% 38: tb_h_fore
% 51: tb_v_aft
% 52: tb_v_fore

for k = 1:size(namelist,1);
    
    hinfo = h5info([address '\' namelist(k,:)]);
    hdfid = [address '\' namelist(k,:)];
    
    dset(k,1) = datenum(namelist(k,21:28),'yyyymmdd')+...
        str2num(namelist(k,30:31))/24+str2num(namelist(k,32:33))/60;
    
    % 06: lat
    lat      = double(h5read(hdfid,'/Global_Projection/cell_lat'));
    % 09: lon
    lon      = double(h5read(hdfid,'/Global_Projection/cell_lon'));
 
    for i = 1:size(lat,1)
        for j = 1:size(lat,2)
            dis(i,j) = sqrt((lon(i,j)-lon_ELBARA)^2+(lat(i,j)-lat_ELBARA)^2);
        end
    end
    
    minVal = min(min(dis));
    [i_p,j_p] = find(dis ==  minVal,1);
    
    
    if dis < 5
%         temp       = double(h5read(hdfid,'/Global_Projection/cell_tb_h_fore'));
%         dset(k,2)  = temp(i_p,j_p);
%         temp       = double(h5read(hdfid,'/Global_Projection/cell_tb_v_fore'));
%         dset(k,3)  = temp(i_p,j_p);
%         temp       = double(h5read(hdfid,'/Global_Projection/cell_tb_h_aft'));
%         dset(k,4)  = temp(i_p,j_p);
%         temp       = double(h5read(hdfid,'/Global_Projection/cell_tb_v_aft'));
%         dset(k,5)  = temp(i_p,j_p);
        fc_lon(k) = lon(i_p,j_p);
        fc_lat(k) = lat(i_p,j_p);
    else
%         dset(k,2:5) = -9999;
        fc_lon(k) = NaN;
        fc_lat(k) = NaN;
    end
    clear temp dis
    
end

clear i j k namelist lat lon i_p i_col hinfo dis num

k       = dset == -9999;
dset(k) = NaN;

save([address '\SMAP_L1C_Maqu_ELBARA.mat'],'dset')

figure(1)
plot(dset(:,1),dset(:,2:5),'.')
title('SMAP L1c brightness temperature data over Maqu ELBARA site')
xlabel('brightness temperature (K)')
ylabel('UTC+00')
datetick('x',2)
% axis([dset(1,1) dset(end,1) min(dset(:,2:5),[],'all')-10 max(dset(:,2:5),[],'all')+10])
axis([dset(1,1) dset(end,1) 150 max(dset(:,2:5),[],'all')+10])
legend('tb h fore','tb v fore','tb h aft','tb v aft',...
    'Location','south','Orientation','horizontal')
legend('boxoff')
plottools

figure(2)
% axesm('MapProjection','lambert',...
%     'MapLonLimit',[min(tibet(:,1))-10, max(tibet(:,1))+10],...
%     'MapLatLimit',[min(tibet(:,2))-10, max(tibet(:,2))+10])
worldmap 'china'
axis off
geoshow('landareas.shp', 'FaceColor', [0.5 1.0 0.5])
% Add Tibet boundary
lat = tibet(:,2);
lon = tibet(:,1);
geoshow(lat, lon, 'Color','k', 'linestyle',':')
geoshow(lat, lon, 'displaytype','polygon', 'edgecolor','b')
% Add Maqu ELBARA point
geoshow(lat_ELBARA, lon_ELBARA, 'Color','r', 'Marker','.','Markersize',14)
% Add center points ploygon
lat = fc_lat;
lon = fc_lon;
geoshow(lat, lon, 'Color','b')
% Set extent
title('SMAP L1C over Maqu ELABRA site')