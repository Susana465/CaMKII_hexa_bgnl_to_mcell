import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

def read_gdat(filename):
    # read gdat file output and put it into a dataframe
    data = pd.read_table(filename, delim_whitespace=True)
    data.columns = data.columns[1:].append(pd.Index(["remove"]))
    return data.drop("remove", axis=1)

# def extract_statistic(data):
#     # function for extracting final concentration [C]
#     stat = data['C'].iloc[-1]
#     print("Final molecule count for column C:")
#     return stat

def extract_statistic(data, molecule, stat_type="last", start=None, end=None):
    try:
        if molecule not in data:
            raise ValueError(f"Molecule '{molecule}' not found in data.") 
         
        if stat_type == "last":
            stat = data[molecule].iloc[-1]

        elif stat_type == "first":
            stat = data[molecule].iloc[0]

        elif stat_type == "range":
            if start is not None and end is not None:
                stat = data[molecule].iloc[start:end]
            else:
                raise ValueError("For 'range' type, 'start' and 'end' must be specified.")
            
        else:
            raise ValueError(f"Unknown stat_type '{stat_type}'. Use 'last', 'first', or 'range'.")
        print(f"Extracted statistic ({stat_type}) for molecule '{molecule}': {stat}")

        return stat
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred while extracting '{stat_type}' from molecule '{molecule}': {e}")
        return None


def extract_parameters(params_dict, param_names):
    """
    Extracts multiple parameters and their values from a pandas DataFrame.

    Arguments:
    - params_dict (pd.DataFrame): DataFrame containing parameter names and values.
    - param_names (list of str): List of parameter names to extract.

    Returns:
    - dict: Dictionary where keys are parameter names and values are extracted values.
    """
    extracted_values = {}
    for param_name in param_names:
        # Locate the parameter in the DataFrame based on its name given by the argument (`param_name`)
        # Use .loc[] to filter rows where 'Parameter' column matches `param_name`
        # compare and select the corresponding value from the 'Value' column.
        parameter = params_dict.loc[params_dict['Parameter'] == param_name, 'Value']
        print(f"Columns in params_dict: {params_dict.columns}")
        # If paremeter not found, print a warning.
        # If the parameter is found,
        # get the first value (iloc[0]) from the filtered result (there should only be one 'kon'); otherwise, return None.
        if parameter.empty:
            print(f"Warning: Parameter '{param_name}' not found.")
            extracted_values[param_name] = None  # Assign None if parameter is missing
        else:
            extracted_values[param_name] = parameter.iloc[0]

    print(f"Extracted parameters: {extracted_values}")
    return extracted_values

def StatsAndParams_to_csv(base_dir, output_file, extract_statistic_func, molecule, stat_type, param_names):
    """
    Iterates through all run folders within a specified base directory, extracts parameters and statistics, 
    and saves them to a CSV file.

    Arguments:
        base_dir (str): The base directory containing the run folders.
        output_file (str): The output CSV file where stats and params will be saved.
        extract_statistic_func (function): Function to extract the statistic from the data.
        molecule (str): The molecule for which statistics are extracted.
        stat_type (str): The type of statistic to extract.
        param_names (list of str): List of parameter names to extract.

    Returns:
        pd.DataFrame: DataFrame containing the extracted parameters and statistics.
    """
    
    # Create an empty dataframe to store params and stats
    #params_stats = pd.DataFrame(columns=param_names + ['statistic'])
    param_stats_list = []
    # Iterate through each folder in the base directory
    for run_folder in [os.path.join(base_dir, dir) for dir in os.listdir(base_dir)]:
        try:
            print(f"Accessing folder: {run_folder}")

            # Locate output data files
            data_files = glob.glob(os.path.join(run_folder, "*_out.gdat"))
            if len(data_files) > 1:
                raise Exception(f"More than one .gdat file in directory {run_folder}")
            if len(data_files) == 0:
                raise Exception(f"No .gdat file in directory {run_folder}")
            
            # Locate parameter files
            param_files = glob.glob(os.path.join(run_folder, "*.csv"))
            if len(param_files) > 1:
                raise Exception(f"More than one .csv file in directory {run_folder}")
            if len(param_files) == 0:
                raise Exception(f"No .csv file in directory {run_folder}")
            
            # Extract data using function defined previously 
            data = read_gdat(data_files[0])  
            statistic = extract_statistic_func(data, molecule = molecule, stat_type = stat_type )  

            # Extract parameters using function defined previously 
            params = pd.read_csv(param_files[0])
            extracted_params = extract_parameters(params, param_names)
            print(f"Successfully extracted_params: {extracted_params}")

            # Add the extracted statistic to the dictionary of extracted parameters
            extracted_params['statistic'] = statistic  # Add statistic to dictionary
            
            param_stats_list.append(extracted_params)

            # Print the extracted parameters as a DataFrame (for debugging purposes).
            print("Extracted parameters for current run:\n", pd.DataFrame([extracted_params]), "\n")

        except Exception as e:
            print(f"Error in folder {run_folder}: {e}")
            continue

    # Convert list of dictionaries to DataFrame
    params_stats = pd.DataFrame.from_records(param_stats_list)
    print(f"This is the params_stats df {params_stats}")
    
    # Save results to CSV
    params_stats.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    return params_stats


def calculate_kd(kon, koff):
    return koff / kon

def compute_kd_and_save(df, output_csv, param_names):
    if not isinstance(param_names, (list, tuple)):  # Ensure param_names is a list or tuple
        raise TypeError("param_names must be a list or tuple of column names.")

    if len(param_names) < 2:
        raise ValueError("param_names must contain at least two elements for kon and koff.")
    
    kon_col, koff_col = param_names[:2]  # Get the first two elements

    # Filter out rows where either kon or koff is NaN or missing
    df_cleaned = df.dropna(subset=[kon_col, koff_col])

    # Calculate 'kd' only for rows without missing values in kon and koff
    df_cleaned["kd"] = calculate_kd(df_cleaned[kon_col], df_cleaned[koff_col])

    # Save the cleaned DataFrame (with kd column) to CSV
    df_cleaned.to_csv(output_csv, index=False)
    print(f"New CSV saved: {output_csv}")


# Define variables:
base_directory = 'D:/data_output_test'
output_csv = 'extracted_statsparams.csv' 
molecule = 'CaMKII_CaM_Ca4_00'
stat_type ='last'
param_names = ['kon_camkii_open', 'koff_camkii_close']
# Having extract_statistic as an argument means 
# I can then call a function that extracts a statistic in a different way to the current one
extract_statistic_func = extract_statistic

# Call and save params and stats in a df:
params_stats_df = StatsAndParams_to_csv(base_directory, output_csv, extract_statistic_func, molecule, stat_type, param_names)

compute_kd_and_save(params_stats_df, "kd_stats.csv", param_names)