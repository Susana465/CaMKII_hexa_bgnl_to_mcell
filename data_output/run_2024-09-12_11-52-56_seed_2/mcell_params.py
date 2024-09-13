import os
import sys
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

def set_up_model():
    
    model = m.Model()

    # Define specific seed
    seed = 2

    # Creating geometry
    vol_cp = 0.50588 # units of um3
    r = (3*vol_cp/(4*np.pi))**(1/3.0) # units of microns

    cp = m.geometry_utils.create_icosphere(
        'CP', radius = r, subdivisions=2)
    cp.is_bngl_compartment = True
    cp.surface_compartment_name = 'PM'
    model.add_geometry_object(cp)

    # Specifies periodicity of visualization output
    for count in model.counts:
        count.every_n_timesteps = 1

    # Do not use bng units:
    model.config.use_bng_units = False

    # Variable parameters
    model.config.time_step = 1e-5 # time steps taken by individual molecules. but this time step is still used by all output statements.
    model.config.seed = seed
    model.config.partition_dimension = 1.5 # 1.5 was before
    model.config.subpartition_dimension = 0.05

    return model