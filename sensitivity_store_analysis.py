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

# Global variable for param_value
parameter_value = None  # Placeholder for extracted parameter value
    
def extract_parameter(params_dict, param_name):
    """
    This function extracts the value of a specific parameter from a pandas DataFrame.
    
    what arguments it takes:
    - params_dict (pd.DataFrame): a DataFrame containing parameter names and values.
    - param_name (str): name of the parameter whose value needs to be extracted.

    what it returns:
    - parameter_value (float or None): value of the parameter if found, else None.
    """

    # Locate the parameter in the DataFrame based on its name given by the argument (`param_name`)
    # Use .loc[] to filter rows where 'Parameter' column matches `param_name`
    # compare and select the corresponding value from the 'Value' column.
    parameter = params_dict.loc[params_dict['Parameter'] == param_name, 'Value']

    print(f"Columns in params_dict: {params_dict.columns}")
    
    # If paremeter not found:
    if parameter.empty:
        print(f"Parameter {param_name} not found.")

    # If the parameter is found,
    # get the first value (iloc[0]) from the filtered result (there should only be one 'kon'); otherwise, return None.
    global parameter_value
    parameter_value = parameter.iloc[0] if not parameter.empty else None
    
    print(f"Extracted value for {param_name}: {parameter_value}")

    return parameter_value


def StatsAndParams_to_csv(base_dir, output_file, extract_statistic_func, molecule, stat_type, param_name):
    """
    This function iterates through all run folders within a specified base directory (data_output/) to save parameters and statistics to a CSV file.

    arguments:
        base_dir (str): The base directory containing the run folders.
        output_file (str): the output CSV file where stats and params will be saved.

    returns:
        pd.DataFrame: param_stats is a dataframe containing the extracted parameters and statistics.
    """
    # Create an empty dataframe to store params and stats
    params_stats = pd.DataFrame(columns=['parameter_value', 'statistic'])

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
            param_value = extract_parameter(params, param_name)

            # Append extracted values to the dataframe
            params_stats = pd.concat([params_stats, pd.DataFrame({'parameter_value': [param_value], 'statistic': [statistic]})], ignore_index=True)
            print(f"Updated params_stats dataframe: {params_stats}")

        except Exception as e:
            print(f"Error in folder {run_folder}: {e}")
            continue

    # Save the results to a CSV file
    params_stats.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    return params_stats

# Define variables:
base_directory = 'data_output'
output_csv = 'extracted_statsparams.csv' 
molecule = 'C'
stat_type ='last'
param_name ='kon'

# Having extract_statistic as an argument means 
# I can then call a function that extracts a statistic in a different way to the current one
extract_statistic_func = extract_statistic

# Call and save params and stats in a df:
params_stats_df = StatsAndParams_to_csv(base_directory, output_csv, extract_statistic_func, molecule, stat_type, param_name)

plt.figure(figsize=(8, 5))
plt.scatter(params_stats_df['parameter_value'], params_stats_df['statistic'], color='blue', alpha=0.7)
plt.xscale('log')  # Logarithmic scale for 'kon'
plt.title('Scatter Plot of kon vs. statistic (Log Scale)')
plt.xlabel('kon (log scale)')
plt.ylabel('Final [C]')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Save the plot to a file
plot_filename = "scatter_plot_kon_vs_statistic.png"  
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')  
print(f"Plot saved as {plot_filename}")

# Show the plot
plt.show()
input("Press Enter to exit...")

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