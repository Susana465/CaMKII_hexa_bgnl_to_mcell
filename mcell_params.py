import os
import sys
import numpy as np
import pandas as pd

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m
print("Import of MCell was successful 3")

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

    #Do not use bng units:
    model.config.use_bng_units = False

    # Variable parameters
    model.config.time_step = 10e-5 # time steps taken by individual molecules. but this time step is still used by all output statements.
    model.config.seed = seed
    model.config.partition_dimension = 1.5 # 1.5 was before
    model.config.subpartition_dimension = 0.05

    return model

def process_parameters(file, folder, timestamp, parameter_overrides=None):
    """
    Load parameters from a (.bngl) file, convert them to a DataFrame, and save to a CSV file.

    Parameters:
    - file: The name of the .bngl file containing parameters.
    - folder: The directory where the .bngl file is located and where output should be saved.
    - timestamp: A string representing the current timestamp, used for naming the output CSV file.
    """
    # Load parameters from the .bngl file, override parameters of hey are there
    param_dict = m.bngl_utils.load_bngl_parameters(
        os.path.join(folder, file),
        parameter_overrides)
    
    ITERATIONS = param_dict.get('ITERATIONS', None)  # Handle cases where 'ITERATIONS' might not be present

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
    
    # Add a column for parameter names
    df['Parameter'] = df.index

    # Define the CSV filename and save the DataFrame to CSV
    csv_filename = os.path.join(folder, f"{timestamp}_parameters.csv")
    df.to_csv(csv_filename, index=False)

    return ITERATIONS, df  # return the ITERATIONS and DataFrame if neededf*/*//**