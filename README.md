# Full Workflow: Running GEOS-Chem for PAH on Kamiak!
# Step 1: Copy the Source Code and Run Directory
Start by copying the GEOS-Chem source code and run directory to your working location:

cp -r /path/to/GCClassic /path/to/my_working_directory/GCClassic

cp -r /path/to/RunDir /path/to/my_working_directory/RunDir

Replace '/path/to/...' with your actual directory paths.
# Step 2: Configure the Run Directory
Navigate to your Run Directory:

cd /path/to/my_working_directory/RunDir

Edit the main input file:

nano input.geos

Update fields like meteorology (MERRA2), METDIR, INPUTDIR, simulation start/end time, timestep and output settings.
# Step 3: Edit HEMCO Configuration (HEMCO_Config.rc)
Open the configuration file:

nano HEMCO_Config.rc

Focus on the PAH emission section. Ensure the line is enabled, paths are correct, and time settings match input.geos.

# Step 4: Load Required Modules
Before building the model, load necessary modules:

module load intel

module load netcdf

module load openmpi
# Step 5: Set Environment Variables
Set the environment for NetCDF and GEOS-Chem:

export NETCDF_ROOT=/data/lab/meng/jahidul/netcdf

export GC_BIN=$NETCDF_ROOT/bin

export GC_F_BIN=$NETCDF_ROOT/bin

export GC_INCLUDE=$NETCDF_ROOT/include

export GC_F_INCLUDE=$NETCDF_ROOT/include

export GC_LIB=$NETCDF_ROOT/lib

export LD_LIBRARY_PATH=$NETCDF_ROOT/lib:$LD_LIBRARY_PATH
# Step 6: Modify and Build the Code
Navigate to the run code directory:

cd /path/to/my_working_directory/RunDir

nano Makefile

Edit CODE_DIR to your code directory path and run:

make -j4 mpbuild

# Step 7: Set the Correct Restart File
Rename the restart file to match your start date:

mv GC_restart.20190701_0000z.nc4 GC_restart.YYYYMMDD_0000z.nc4
# Step 8: Create a Batch Script
# Step 9: Delete existing diaginfo.dat and tracerinfo.dat
rm diaginfo.dat tracerinfo.dat
# Step 10: Submit Your Job






