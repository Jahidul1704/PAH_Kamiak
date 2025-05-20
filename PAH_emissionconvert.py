import os
import numpy as np
from netCDF4 import Dataset

# Define the constant for multiplication
constant = 3.80265176e-16

# Define fixed time values
fixed_time_values = np.array([0.0, 31.0, 60.0, 91.0, 121.0, 152.0, 182.0, 213.0, 244.0, 274.0, 305.0, 335.0])

# Define folder paths
input_folder_path = '/Users/jahidulislam/Downloads/Datanew/PAH'
intermediate_output_folder_path = '/Users/jahidulislam/Downloads/GEMS/PAH2'
final_output_folder_path = '/Users/jahidulislam/Downloads/GEMS/nc_month/PAH2'

# Step 1: Multiply 'emission' by constant and save to intermediate folder
nc_files = [f for f in os.listdir(input_folder_path) if f.endswith('.nc')]

for nc_file in nc_files:
    input_file_path = os.path.join(input_folder_path, nc_file)
    output_file_path = os.path.join(intermediate_output_folder_path, f"{nc_file}")

    with Dataset(input_file_path, 'r') as file:
        emission = file.variables['emission'][:]
        emission_converted = emission * constant

        with Dataset(output_file_path, 'w', format='NETCDF4') as output_file:
            for name, dimension in file.dimensions.items():
                output_file.createDimension(name, len(dimension))

            for name, variable in file.variables.items():
                if name != 'emission':
                    var = output_file.createVariable(name, variable.datatype, variable.dimensions)
                    var[:] = variable[:]

            emission_var = output_file.createVariable('emission', 'f4', ('time', 'lat', 'lon'))
            emission_var[:] = np.transpose(emission_converted, (2, 1, 0))
            emission_var.setncattr('units', 'kg/m2/s')

    print(f"Step 1 completed: Converted and saved to: {output_file_path}")

# Step 2: Modify structure and attributes, save to final folder
nc_files = [f for f in os.listdir(intermediate_output_folder_path) if f.endswith('.nc')]

for nc_file in nc_files:
    input_file_path = os.path.join(intermediate_output_folder_path, nc_file)
    output_file_path = os.path.join(final_output_folder_path, f"{nc_file}")

    with Dataset(input_file_path, 'r') as dataset:
        with Dataset(output_file_path, 'w', format='NETCDF4') as new_dataset:
            # Create dimensions
            new_dataset.createDimension('time', len(fixed_time_values))  # fixed 12 time points
            new_dataset.createDimension('lon', len(dataset.dimensions['lon']))
            new_dataset.createDimension('lat', len(dataset.dimensions['lat']))

            # Create time variable and set fixed values
            time_var = new_dataset.createVariable('time', 'f4', ('time',), chunksizes=(1,))
            time_var[:] = fixed_time_values
            time_var.standard_name = "time"
            time_var.long_name = "time"
            time_var.units = "days since 2014-01-01 00:00:00"
            time_var.calendar = "standard"
            time_var.axis = "T"

            # Create and copy lon variable
            lon_var = new_dataset.createVariable('lon', 'f4', ('lon',), chunksizes=(1800,))
            lon_var[:] = dataset.variables['lon'][:]
            lon_var.standard_name = "longitude"
            lon_var.long_name = "longitude"
            lon_var.units = "degrees_east"
            lon_var.axis = "X"

            # Create and copy lat variable
            lat_var = new_dataset.createVariable('lat', 'f4', ('lat',), chunksizes=(1800,))
            lat_var[:] = dataset.variables['lat'][:]
            lat_var.standard_name = "latitude"
            lat_var.long_name = "latitude"
            lat_var.units = "degrees_north"
            lat_var.axis = "Y"

            # Create emission variable
            emission_var = new_dataset.createVariable('emission', 'f4', ('time', 'lat', 'lon'),
                                                       chunksizes=(1, 1800, 3600))
            emission_data = dataset.variables['emission'][:]
            emission_var[:] = emission_data
            emission_var.long_name = "emission"
            emission_var.units = "kg m-2 s-1"
            emission_var.cell_methods = "time: mean sector: mean"

    print(f"Step 2 completed: Final NetCDF file saved to: {output_file_path}")
