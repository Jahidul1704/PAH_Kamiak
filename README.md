# Full Workflow: Running GEOS-Chem on Kamiak!
# Step 1: Copy the Source Code and Run Directory
Start by copying the GEOS-Chem source code and run directory to your working location:

'cp -r /path/to/GCClassic /path/to/my_working_directory/GCClassic'

"cp -r /path/to/RunDir /path/to/my_working_directory/RunDir"

Replace '/path/to/...' with your actual directory paths.
# Step 2: Configure the Run Directory
Navigate to your Run Directory:

'cd /path/to/my_working_directory/RunDir'

Edit the main input file:

'nano input.geos'

Update fields like meteorology (MERRA2), METDIR, INPUTDIR, simulation start/end time, and output settings.

