import os
import pandas as pd
import glob
import numpy as np
from sensitivity_store_analysis import read_gdat
from sensitivity_store_analysis import extract_statistic

"""
This script processes simulation output data for multiple experimental runs, extracting both input parameters
and output statistics, and compiles them into a single CSV summary file for further analysis.

Key steps performed by the script:
1. Iterates over all run folders located in the specified `base_dir`.
2. For each run:
   - Extracts metadata such as run ID, date, and random seed from the folder name.
   - Reads the associated parameters CSV file (if present), storing parameter-value pairs.
   - Locates and processes the corresponding `.gdat` file to extract a specific statistical value
     (e.g., the last value of the `CaMKII_open` molecule time series).
   - Adds all collected information to a dictionary representing one run.
3. Aggregates all run data into a pandas DataFrame.
4. Writes the aggregated data to a CSV file defined by `output_csv`.

This output file provides an overview of simulation settings and results, useful for sensitivity analysis
or comparison across different conditions.
"""


# Define the base directory and the output CSV path
base_dir = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/thesis_results/NMDAR_MT_open_and_close_release'
output_csv = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/thesis_results/NMDAR_MT_open_and_close_release/Parameters_Overview.csv'

# Initialize a list to store the data from all runs
data = []
molecule = "CaMKII_open"

# Iterate through each run directory
for run_folder in os.listdir(base_dir):
    run_path = os.path.join(base_dir, run_folder)
    if os.path.isdir(run_path):
        run_id = run_folder
        date, seed = run_id.split('_')[1], run_id.split('_')[-1]
        print(f"Processing run: {run_id}, Date: {date}, Seed: {seed}")
        
        # Locate the parameters.csv file
        param_file = [f for f in os.listdir(run_path) if f.endswith('_parameters.csv')]
        
        if param_file:
            param_file_path = os.path.join(run_path, param_file[0])
            print(f"Found parameters file: {param_file_path}")

            # Read parameters.csv into a DataFrame
            try:
                param_df = pd.read_csv(param_file_path, sep=',', header=None, names=['Value', 'Parameter'])
            except Exception as e:
                print(f"Error loading CSV file: {e}")
                continue

            param_dict = dict(zip(param_df['Parameter'], param_df['Value']))

        # Attempt to find the .gdat file in the current run folder
        gdat_files = glob.glob(os.path.join(run_path, "*.gdat"))
        if gdat_files:
            gdat_file_path = gdat_files[0]            
            # Check if the .gdat file is empty
            if os.path.getsize(gdat_file_path) == 0:
                print(f".gdat file {gdat_file_path} is empty. Skipping.")
                param_dict[molecule] = np.nan
            else:
                gdat_data = read_gdat(gdat_file_path)
                stat = extract_statistic(gdat_data, molecule, stat_type="last")
                print(f"Extracted statistic for {molecule}: {stat}")
                param_dict[molecule] = stat

        run_data = {'Run ID': run_id, 'Date': date, 'Seed': seed}
        run_data.update(param_dict)
        data.append(run_data)

# Convert the collected data into a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv, index=False)

print(f'Parameters overview has been saved to {output_csv}.')
