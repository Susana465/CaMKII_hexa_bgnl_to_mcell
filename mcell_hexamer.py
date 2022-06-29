import os
import sys
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

viz_output = m.VizOutput(
    './viz_data/seed_00001/Scene',
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
    'hexamer_20220624.bngl', 
    observables_path_or_file='out.gdat')

#open bngl file and load the parameters into a dictionary
param_dict = m.bngl_utils.load_bngl_parameters('hexamer_20220624.bngl')
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
model.config.time_step = 1e+2

model.config.partition_dimension = 1.5 # 1.5 was before
model.config.subpartition_dimension = 0.05

model.initialize()

model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()