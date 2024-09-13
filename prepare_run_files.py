# This is the script where I prepare folders and call mcell and bngl params that may vary.
# Parameters are to be changed in the [define_simulation_params.py] file, not here.
import os
import sys
import numpy as np
from datetime import datetime
import pandas as pd
import shutil  # for easier file copying

# Call the function "set_up_model" that runs mcell model with params specs from define_simulation_params.py
from mcell_params import set_up_model

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

def prepare_out_folder(folder_name, seed, files_to_copy=["file.bngl", "file.py"]):
    
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.join(folder_name, f"run_{timestamp}_seed_{seed}")

    # Create the timestamped folder
    os.makedirs(folder_name)

    # Loop over each file and copy it to the destination folder
    for file_name in files_to_copy:
        dest_file = os.path.join(folder_name, file_name)  # Destination path with original name
        shutil.copy(file_name, dest_file)  # Copy the file with original name
    
    print(f"Files will be saved in {folder_name}.")

    return folder_name, timestamp

model = set_up_model()

# Define what files I am using here:
bngl_file = "dodecamer.bngl"
mcell_param_file = "mcell_params.py"

# Call the function and capture the path to the run folder and timestamp
run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, [bngl_file, mcell_param_file])

# Save viz_data under timestamped folder
# viz_output = m.VizOutput(
#     os.path.join(run_folder, f"viz_data/Scene_"),
#     every_n_timesteps= 100
#     )
# model.add_viz_output(viz_output)

# Load copied bngl file and save it
model.load_bngl(
    os.path.join(run_folder, bngl_file), 
    observables_path_or_file = os.path.join(run_folder, f"{timestamp}_out.gdat"))

def process_parameters(file, folder, timestamp):
    """
    Load parameters from a (.bngl) file, convert them to a DataFrame, and save to a CSV file.

    Parameters:
    - file: The name of the .bngl file containing parameters.
    - folder: The directory where the .bngl file is located and where output should be saved.
    - timestamp: A string representing the current timestamp, used for naming the output CSV file.
    """
    # Load parameters from the .bngl file
    param_dict = m.bngl_utils.load_bngl_parameters(os.path.join(folder, file))
    ITERATIONS = param_dict.get('ITERATIONS', None)  # Handle cases where 'ITERATIONS' might not be present

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
    
    # Add a column for parameter names
    df['Parameter'] = df.index

    # Define the CSV filename and save the DataFrame to CSV
    csv_filename = os.path.join(folder, f"{timestamp}_parameters.csv")
    df.to_csv(csv_filename, index=False)

    return ITERATIONS, df  # return the ITERATIONS and DataFrame if needed

ITERATIONS, df = process_parameters(bngl_file, run_folder, timestamp)

# Check to see if total iterations is defined as a global parameter
if 'ITERATIONS' not in globals():
        ITERATIONS = 100

# Total_Iterations if not defined explicitly default to 1e-6
model.config.total_iterations = ITERATIONS

# Initialize, export, and run the model
model.initialize()

#model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()