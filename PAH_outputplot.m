   
% Define the file path
mainpath = '/Users/jahidulislam/Downloads'; % Change to your local path
filePath = '/Users/jahidulislam/Downloads/GeoHealth_Sup/GC_run_directories/rundir_200220_A/geosfp_4x5_pah_FRESH/output_from_bpch.nc';
%filePath = '/Users/jahidulislam/PAH_Project/Output/201407/output_from_bpch201407.nc';
shapepath   = sprintf('%s/data/worldboundaries/World_Countries_shp',mainpath); %province border files
shapepath1   = sprintf('%s/data/province',mainpath); %province border files

% Read the dimensions and variables from the NetCDF file
lon = ncread(filePath, 'lon'); % Longitude
lat = ncread(filePath, 'lat'); % Latitude
pm25 = ncread(filePath, 'IJ_AVG_S_FLA'); % PM2.5 data
Air_d=ncread(filePath, 'BXHGHT_S_AIRNUMDE');
time = ncread(filePath, 'time');
Air_de1 = squeeze(Air_d(1, :, :, 1));
Air_de_base = 1e6.* Air_de1;
% Extract PM2.5 at the base level (level 1)
pm25_base1 = squeeze(pm25(1, :, :, 1)); % Dimensions: lon x lat at level 1
factor=(202.31/(6.023e23)).*Air_de_base;

pm25_base = factor.* pm25_base1;
% Define the output Excel file path
%excelFilePath = '/Users/jahidulislam/PAH_Project/Output/201407/pm25_base_output.xlsx';

% Write the PM2.5 base data to Excel
%writematrix(pm25_base, excelFilePath);

% Create a meshgrid for plotting
[Lon, Lat] = meshgrid(lon, lat);

% Ensure that the pm25_base data is correctly shaped (it should match the grid size)
if size(pm25_base, 1) ~= size(Lon, 1) || size(pm25_base, 2) ~= size(Lat, 1)
    pm25_base = pm25_base'; % Transpose if needed
end

% Plot the PM2.5 data
figure;
pcolor(Lon, Lat, pm25_base'); % Use transposed pm25_base
shading interp;
colorbar;
title('BAP Concentrations(ng/m3) at Base Level 2x25 in July 2019', 'FontWeight', 'bold', 'FontSize', 14);
xlabel('Longitude', 'FontWeight', 'bold', 'FontSize', 14);
ylabel('Latitude', 'FontWeight', 'bold', 'FontSize', 14);
 % Color limits
gcalim = {[1e-4 10]};  % From 0.0001 to 10

% Apply color limits
caxis(gcalim{1});

% Set logarithmic color scale
set(gca, 'ColorScale', 'log');

% Customize colorbar tick marks
cb = colorbar;
cb.Ticks = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10];
cb.TickLabels = string(cb.Ticks);  % Optional, to ensure formatting

% Optional: grid on
grid on;



% Enhance visualization with country boundaries
S = shaperead(sprintf('%s/PROVINCE.SHP', shapepath1), 'UseGeoCoords', true); % Import province border files
states = shaperead('usastatehi', 'UseGeoCoords', true); % US states border files

% Show Canada Province Boundary
for iii = 1:13
    geoshow(flipud(S(iii).Lat), flipud(S(iii).Lon), 'DisplayType', 'polygon', 'FaceColor', [1 1 1], 'FaceAlpha', 0.1);
end
for iii = 1:51
    geoshow(flipud(states(iii).Lat), flipud(states(iii).Lon), 'DisplayType', 'polygon', 'FaceColor', [1 1 1], 'FaceAlpha', 0.1);
end

% Read and plot country boundaries from the shapefile
countries = shaperead(shapepath, 'UseGeoCoords', true);
for k = 1:length(countries)
    geoshow(countries(k).Lat, countries(k).Lon, 'DisplayType', 'polygon', 'FaceColor', 'none', 'EdgeColor', 'black');
end

colormap parula; % Choose a color map
 %colormap summer;
