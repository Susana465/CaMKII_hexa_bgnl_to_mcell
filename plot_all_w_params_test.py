import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterSciNotation
import pandas as pd

def extract_parameters(params_dict, param_names):
    """
    Extracts multiple parameters and their values from a pandas DataFrame.
    """
    extracted_values = {}
    for param_name in param_names:
        # Locate the parameter in the DataFrame based on its name
        parameter = params_dict.loc[params_dict['Parameter'] == param_name, 'Value']
        if parameter.empty:
            print(f"Warning: Parameter '{param_name}' not found.")
            extracted_values[param_name] = None
        else:
            extracted_values[param_name] = parameter.iloc[0]

    return extracted_values

def plot_multiple_gdat(target_folder, selected_variables=None, param_names=None):
    """
    Reads and plots data from .gdat files in the specified folder.
    """
    plt.figure(figsize=(10, 6))  # Adjust figure size
    fmt = LogFormatterSciNotation()

    # Initialize lists to store data for sorting
    all_lines = []  # Store line objects for sorting by color
    all_labels = []  # Store the corresponding labels
    all_kon = []  # Store `kon` values for sorting

    # **Custom Color Mapping Based on `kon` Values**
    # Manually define color thresholds for kon values
    def get_color_for_kon(kon_value):
        """
        Returns a color based on the `kon` value.
        """
        if kon_value >= 1e4:  
            return "rebeccapurple"  
        elif kon_value >= 1e3:  
            return "mediumslateblue"  
        elif kon_value >= 1e2:  
            return "lavender"  
        else:  
            return "lightsteelblue"  

    for root, dirs, files in os.walk(target_folder):
        csv_filepath = None

        # Scan for a CSV file to extract parameters
        for file in files:
            if file.endswith(".csv"):
                csv_filepath = os.path.join(root, file)
                break

        # Extract parameters if CSV file exists
        if csv_filepath and os.path.exists(csv_filepath):
            params_dict = pd.read_csv(csv_filepath)
            extracted_params = extract_parameters(params_dict, param_names)
        else:
            extracted_params = {}

        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                # Load the data
                data = np.loadtxt(fname=target_filepath)
                if data.ndim == 1:
                    print(f"Warning: {file} appears to have an unexpected format. Skipping.")
                    continue

                # Extract header
                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.split()[2:]

                # Ensure selected variables are mapped
                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}
                if selected_variables is None:
                    selected_variables = list(header_dict.keys())
                else:
                    selected_variables = [var.lower() for var in selected_variables]

                # Build the legend label from the extracted parameters
                if extracted_params:
                    legend_label = " - ".join([f"{param}: $10^{{{int(np.log10(value))}}}$"
                        if isinstance(value, (int, float)) and value > 0
                        else f"{param}: {value}"
                        for param, value in extracted_params.items() if value is not None])
                else:
                    legend_label = file  # Use filename if no CSV was found

                # Get `kon` value for color mapping (assuming `kon` is in extracted_params)
                kon_value = extracted_params.get("kon_camkii_open", 1)  # Default to 1 if not found
                all_kon.append(kon_value)  # Store `kon` value for sorting

                print(f"kon_value extracted: {kon_value}")  # Debugging

                # Plot each selected variable and store the line, label, and `kon`
                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        line, = plt.plot(data[:, 0], data[:, idx], label=legend_label)

                        # Get the color for the line based on `kon` value**
                        line.set_color(get_color_for_kon(kon_value))  # Set the color manually based on `kon`
                        all_lines.append(line)
                        all_labels.append(legend_label)
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Sort lines by `kon` values
    sorted_indices = np.argsort(all_kon)  # Get sorted indices based on `kon` values
    all_lines_sorted = [all_lines[i] for i in sorted_indices]  # Sort lines
    all_labels_sorted = [all_labels[i] for i in sorted_indices]  # Sort corresponding labels

    # Customize plot
    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")

    # Set background color to grey
    plt.gca().set_facecolor('lightgrey')
    
    plt.grid(True)
    plt.tight_layout()

    # Adjust legend and its position
    plt.legend(all_lines_sorted, all_labels_sorted, title="Simulation Runs ($k_{D}$ = 500 M)", loc="upper left")
    
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
