import os
import sys
import numpy as np
from datetime import datetime

def save_run_iteration(folder_name, timestamp):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Generate the filename
    filename = f"{folder_name}/dodecamer_run_{timestamp}.py"
    
    # Save the content of the current python script into a timestamped filename
    with open(__file__, 'r') as f:
        content = f.read()
        with open(filename, 'w') as new_f:
            new_f.write(content)

    # Copy the bngl file being used to the generated timestamped filename
    with open("test_ABC.bngl", 'r') as src_file, open(bngl_filename, 'w') as dest_file:
        dest_file.write(src_file.read())

# create a string name containing date to use for output files and folders
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create the timestamped run folder
run_folder = f"run_{current_datetime}"
os.makedirs(run_folder)

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

viz_output = m.VizOutput(
    os.path.join(run_folder, f"viz_data/seed_00001/Scene_{current_datetime}"),
    every_n_timesteps= 100
    )

# Creting geometry
vol_cp = 0.50588 # units of um3
r = (3*vol_cp/(4*np.pi))**(1/3.0) # units of microns

cp = m.geometry_utils.create_icosphere(
    'CP', radius = r, subdivisions=2)
cp.is_bngl_compartment = True
cp.surface_compartment_name = 'PM'

model = m.Model()

model.add_viz_output(viz_output)
model.add_geometry_object(cp)

model.load_bngl(
    'dodecamer.bngl', 
    observables_path_or_file = os.path.join(run_folder, f"{current_datetime}_out.gdat"))

#open bngl file and load the parameters into a dictionary
param_dict = m.bngl_utils.load_bngl_parameters('dodecamer.bngl')
ITERATIONS = param_dict['ITERATIONS']

# Specifies periodicity of visualization output
for count in model.counts:
    count.every_n_timesteps = 1

#Do not use bng units:
model.config.use_bng_units = False

# Check to see if total iterations is defined as a global parameter
if 'ITERATIONS' not in globals():
    ITERATIONS = 100

# Total_Iterations if not defined explicitly default to 1e6
model.config.total_iterations = ITERATIONS
model.config.time_step = 1e-4

model.config.partition_dimension = 1.5 # 1.5 was before
model.config.subpartition_dimension = 0.05

model.initialize()

model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()

# Save files into timestamped directory
save_run_iteration(run_folder, current_datetime)