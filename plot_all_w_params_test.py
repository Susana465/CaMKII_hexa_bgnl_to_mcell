import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterSciNotation
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as mcolors

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
    
    # Create a colormap for `kon` values
    cmap = cm.get_cmap("Blues")  # Use the "Blues" colormap
    norm = mcolors.Normalize(vmin=0, vmax=1)  # Normalize to range [0, 1] for the colormap
    
    # First pass: collect all `kon` values to normalize the colormap
    kon_values = []

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
                kon_values.append(kon_value)  # Collect all `kon` values

                print(f"kon_value extracted: {kon_value}")  # Debugging

                # Plot each selected variable and store the line, label, and `kon`
                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        all_labels.append(legend_label)
                        all_kon.append(kon_value)  # Store `kon` value for sorting
                        line, = plt.plot(data[:, 0], data[:, idx], label=legend_label)
                        all_lines.append(line)
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Ensure we have valid kon_values and lines
    print(f"All kon values: {kon_values}")  # Debugging
    if not kon_values:
        print("Error: No kon values were extracted. Plotting cannot proceed.")
        return

    # Normalize the `kon` values to the range [0, 1] for the colormap
    norm = mcolors.Normalize(vmin=min(kon_values), vmax=max(kon_values))
    print(f"Normalized kon range: {min(kon_values)} to {max(kon_values)}")  # Debugging

    # Apply color based on `kon` values
    for line, kon_value in zip(all_lines, all_kon):
        color = cmap(norm(kon_value))  # Map `kon` value to color
        line.set_color(color)

    # Sort lines by `kon` (darker color = higher `kon`)
    sorted_indices = np.argsort(all_kon)[::-1]  # Sort in descending order
    sorted_lines = [all_lines[i] for i in sorted_indices]
    sorted_labels = [all_labels[i] for i in sorted_indices]

    # Adjust the legend to match the sorted lines
    plt.legend(sorted_lines, sorted_labels, title="Simulation Runs (sorted by $k_{on}$)", loc="upper left")
    
    # Customize plot
    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")
    plt.grid(True)
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
