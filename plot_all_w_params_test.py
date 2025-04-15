import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterSciNotation
import matplotlib.ticker as mticker
import pandas as pd

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
            try:
                extracted_values[param_name] = float(parameter.iloc[0])
            except ValueError:
                extracted_values[param_name] = parameter.iloc[0]

    print(f"Extracted parameters: {extracted_values}")
    return extracted_values

color_dict={"kon_camkii_open: 2.00e+04 - koff_camkii_close: 1.00e+07":"blue", 
            "kon_camkii_open: 2.00e+02 - koff_camkii_close: 1.00e+05":"green",
            "kon_camkii_open: 2.00e+03 - koff_camkii_close: 1.00e+06":"red"}

def plot_multiple_gdat(target_folder, selected_variables=None, param_names=None):
    """
    Reads and plots data from .gdat files in the specified folder,
    can iteratively go through multiple subfolders.
    
    Parameters:
    target_folder (str): Path to the folder containing .gdat files.
    selected_variables (list of str, optional): Variables to plot. If None, all variables are plotted.
    param_names (list of str, optional): List of parameter names to extract for the legend.
    """

    plt.figure(figsize=(10, 6))  # Adjust figure size

    # Tranforming numbers to power of 10 scientific notation
    #f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
    #g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    
    #fmt = mticker.FuncFormatter(g)

    fmt = LogFormatterSciNotation()

    for root, dirs, files in os.walk(target_folder):
        csv_filepath = None

        # Scan every file in the current folder
        for file in files:
            if file.endswith(".csv"):
                csv_filepath = os.path.join(root, file)
                break  # just take the first CSV file you find (we assume there is only one)

        # If both are true, we load it into params_dict using pandas. 
        if csv_filepath and os.path.exists(csv_filepath):
            params_dict = pd.read_csv(csv_filepath)
            extracted_params = extract_parameters(params_dict, param_names)
            print(f"Extracted parameters from {csv_filepath}: {extracted_params}")

            #if kon = 2, give it the blue colour

            # Convert extracted parameter values to scientific notation (1x10^6)
            #for param, value in extracted_params.items():
            #    if isinstance(value, (int, float)):  # Only format numeric values
            #        # Format each value into scientific notation
            #        extracted_params[param] = f"{value:.2e}"
                    
        else:
            extracted_params = {} 
            print("Warning: No CSV file found. Skipping parameter extraction.")     

        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                # Load the data
                data = np.loadtxt(fname=target_filepath)

                # Ensure data is 2D (skip if it's not)
                if data.ndim == 1:
                    print(f"Warning: {file} appears to have an unexpected format. Skipping.")
                    continue

                # Extract header
                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    print(f"Header in {file}: {first_line}")  # Debugging
                    header = first_line.split()[2:]  # Adjust if necessary

                # Ensure headers are correctly mapped
                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}
                print(f"Parsed headers: {header_dict}")  # Debugging

                # Convert user input to lowercase for case-insensitive matching
                if selected_variables is None:
                    selected_variables = list(header_dict.keys())
                else:
                    selected_variables = [var.lower() for var in selected_variables]
                
                # Build legend using extracted parameters, if available
                if extracted_params:
                     #legend_label = " - ".join(["{param}: {value_10}".format(value_10=fmt(value),param=param) for param, value in extracted_params.items() if value is not None])
                     legend_label = " - ".join([
                        f"{param}: {fmt.format_data(value)}"
                        if isinstance(value, (int, float)) and value > 0
                        else f"{param}: {value}"
                        for param, value in extracted_params.items() if value is not None
                    ])

                     key = " - ".join([
                         f"{param}: {value}" 
                         for param, value in extracted_params.items() if value is not None])
                else:
                    legend_label = file  # If no CSV was found, use the filename as the legend label

                # Plot each selected variable
                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        plt.plot(data[:, 0], data[:, idx], 
                                 label=legend_label)
                        print(legend_label)
                        print(key) #color=color_dict[key])
                        
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Customize plot
    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1))
    # Adjust layout to make space for the legend
    plt.tight_layout()

    # Save as PNG
    output_png_filepath = os.path.join(target_folder, "all_variables_plot.png")
    plt.savefig(output_png_filepath, dpi=500)
    plt.show()

    print(f"Your combined plot has been saved as {output_png_filepath}")


if __name__ == "__main__":
    """
    Main execution block that prompts user for input and calls the plot function.
    """
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]  # Clean whitespace

    # Ask user for which parameter names to include in legend
    selected_param_input = input("Enter parameter names to use in the legend (from the CSVs), separated by commas (or press Enter to skip): ")
    selected_param_names = [p.strip() for p in selected_param_input.split(",") if p.strip()]

    # Now call the plot function with everything
    plot_multiple_gdat(target_folder, selected_variables, selected_param_names)