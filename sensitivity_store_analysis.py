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

            # Extract metadata from folder name
            run_id = os.path.basename(run_folder)
            try:
                date, seed = run_id.split('_')[1], run_id.split('_')[-1]
                print(f"Processing run: {run_id}, Date: {date}, Seed: {seed}")
            except IndexError:
                print(f"Warning: Unable to extract date and seed from run ID {run_id}")
                date, seed = None, None

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

            # Add the extracted statistic and metadata to the dictionary of extracted parameters
            extracted_params['statistic'] = statistic
            extracted_params['Run ID'] = run_id
            extracted_params['Date'] = date
            extracted_params['Seed'] = seed

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
base_directory = 'data_output'
output_csv = 'extracted_statsparams_2.csv' 
molecule = 'C'
stat_type ='last'
param_names = ['kon222', 'koff']

# Having extract_statistic as an argument means 
# I can then call a function that extracts a statistic in a different way to the current one
extract_statistic_func = extract_statistic

# Call and save params and stats in a df:
params_stats_df = StatsAndParams_to_csv(base_directory, output_csv, extract_statistic_func, molecule, stat_type, param_names)

#compute_kd_and_save(params_stats_df, "kd_stats.csv", param_names)

#----
# def plot_kd_vs_statistic(csv_file):
#     # Load the CSV file
#     df = pd.read_csv(csv_file)

#     # Check if the required columns exist
#     if "kd" not in df.columns or "statistic" not in df.columns:
#         raise ValueError("CSV file must contain 'kd' and 'statistic' columns.")

#     # Scatter plot
#     plt.figure(figsize=(8, 6))
#     plt.scatter(df["kd"], df["statistic"], color="blue", alpha=0.7)
#     plt.xlabel("Kd (koff / kon)")
#     plt.ylabel("Statistic Value")
#     plt.title("Kd vs Statistic")
#     plt.xscale("log")  # Log scale for better visualization
#     plt.grid(True, which="both", linestyle="--", linewidth=0.5)
#     plt.show()

# # Example usage
# plot_kd_vs_statistic("kd_stats.csv")

# plt.figure(figsize=(8, 5))
# plt.scatter(params_stats_df[param_name], params_stats_df['statistic'], color='blue', alpha=0.7)
# plt.xscale('log')  # Logarithmic scale for 'kon'
# plt.title('Scatter Plot of kon vs. statistic (Log Scale)')
# plt.xlabel('kon (log scale)')
# plt.ylabel('Final [C]')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# # Save the plot to a file
# plot_filename = "scatter_plot_kon_vs_statistic.png"  
# plt.savefig(plot_filename, dpi=300, bbox_inches='tight')  
# print(f"Plot saved as {plot_filename}")

# # Show the plot
# plt.show()
# input("Press Enter to exit...")

# # Create an empty dataframe to store params and stats
# params_stats = pd.DataFrame(columns=['kon', 'statistic'])
# print(params_stats) #should be empty at this point

# # for any directory structure, pull all params we've used an the stats we have defined as above

# for run_folder in [os.path.join('data_output', dir) for dir in os.listdir('data_output')]:
#     try:
#         print(f"Accessing folder: {run_folder}")
#         # Read output data and store statistics
#         data_files = glob.glob(os.path.join(run_folder, "*_out.gdat"))
#         if len(data_files) > 1:
#             raise Exception(f"More than one .gdat file in directory {run_folder}")
#         if len(data_files) == 0:
#             raise Exception(f"No .gdat file in directory {run_folder}")
        
#         # Read parameters in csv file and store values
#         param_files = glob.glob(os.path.join(run_folder, "*.csv"))
#         if len(param_files) > 1:
#             raise Exception(f"More than one .csv file in directory {run_folder}")
#         if len(param_files) == 0:
#             raise Exception(f"No .csv file in directory {run_folder}")
        
#         # If files are found, proceed with processing
#         # For the statistic
#         data = read_gdat(data_files[0])
#         statistic = extract_statistic(data) #use function defined above for extracting stat

#         # For the parameter:
#         params = pd.read_csv(param_files[0])
#         print(f"This is whats in params: {params}")

#         kon_value = extract_parameter(params, 'kon')
#         print(f"This is the kon_value: {kon_value}")

#         # Add to the dataframe using pd.concat
#         params_stats = pd.concat([params_stats, pd.DataFrame({'kon': [kon_value], 'statistic': [statistic]})], ignore_index=True)
#         print(f"This is the params_stats dataframe: {params_stats}")

#     # Continue to the next folder despite the error    
#     except Exception as e:
#         print(f"Error in folder {run_folder}: {e}")
#         continue

# params_stats.to_csv('extracted_statistics.csv', index=False)

#     #for data_file in data_files:
#         # data = read_gdat(data_file)
#         # statistic = extract_statistic(data)
#         # # Store the parameters and statistic
#         # result = pd.DataFrame({
#         #     'kon': [kon],
#         #     'statistic': [statistic]
#         # })
#         # params_stats = pd.concat([params_stats, result], ignore_index=True)

# # Plot the results
# # plt.figure(figsize=(10, 6))
# # plt.plot(params_stats['kon'], params_stats['statistic'], marker='o', linestyle='-')
# # plt.xlabel('kon')
# # plt.ylabel('Statistic')
# # plt.title('kon vs Statistic')
# # plt.grid(True)
# # plt.show()

# # https://mcell.org/tutorials/scripting/customization.html 

# #i want mcell to run with different kon that i input here, 
# # for kon in [10, 100, 1000, 10000]:
# #     #create function run_model, with all specified values in the model, except for this one here that i am interested in
# #     run_model(kon = kon)

# # # read all the param files and data file, extract final [C] (use os.glob)
# # for files in all_files: #(use os.glob)
# #     parameters = pd.read_csv(parameter_file)
# #     data = read_gdat(data_file)
# #     statistic = extract_statistic(data)
# #     params_stats = pd.concat(params_stats,parameters,statistic)

# #give me a .gdat file output
# # access each gdat stat for each kon, create a dataframe which stores the stats I am interested in recording

# # General Workflow:
# # Loop Over kon Values:
# # You'll need to run the model with different kon values. The run_model() function is responsible for running the simulation with the specified kon value.

# # Reading Output Files:
# # After each model run, you'll need to read the resulting .gdat file, extract the statistic (e.g., the final concentration [C]), and store this information in a DataFrame.

# # Create a DataFrame:
# # You’ll store the statistics (kon and the extracted concentration) for each model run in a DataFrame.

# # Plot the Results:
# # After collecting all the statistics, you'll plot how the concentration changes with respect to kon.