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
        parameter = params_dict.loc[params_dict['Parameter'] == param_name, 'Value']
        print(f"Columns in params_dict: {params_dict.columns}")
        if parameter.empty:
            print(f"Warning: Parameter '{param_name}' not found.")
            extracted_values[param_name] = None
        else:
            extracted_values[param_name] = parameter.iloc[0]
    print(f"Extracted parameters: {extracted_values}")
    return extracted_values

def plot_multiple_gdat(target_folder, selected_variables=None, param_names=None):
    """
    Reads and plots data from .gdat and .csv files in the specified folder.
    """
    plt.figure(figsize=(10, 6))
    fmt = LogFormatterSciNotation()

    all_lines = []
    all_labels = []
    all_kon = []

    def get_color_for_kon(kon_value):
        if kon_value >= 1e6:
            return "rebeccapurple"
        elif kon_value >= 1e5:
            return "mediumslateblue"
        elif kon_value >= 1e4:
            return "lightslategrey"
        else:
            return "blue"

    for root, dirs, files in os.walk(target_folder):
        csv_filepath = None
        for file in files:
            if file.endswith(".csv"):
                csv_filepath = os.path.join(root, file)
                break

        if csv_filepath and os.path.exists(csv_filepath):
            params_dict = pd.read_csv(csv_filepath)
            extracted_params = extract_parameters(params_dict, param_names)
        else:
            extracted_params = {}

        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                data = np.loadtxt(fname=target_filepath)
                if data.ndim == 1:
                    print(f"Warning: {file} appears to have an unexpected format. Skipping.")
                    continue

                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.split()[2:]

                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}
                if selected_variables is None:
                    selected_variables = list(header_dict.keys())
                else:
                    selected_variables = [var.lower() for var in selected_variables]

                # Build the legend label
                kon = extracted_params.get("kon_CaMKII_NMDAR")
                koff = extracted_params.get("koff_CaMKII_NMDAR")
                if kon is not None and koff is not None and kon > 0:
                    kd = koff / kon
                    if kd > 0:
                        mantissa = kd / (10 ** np.floor(np.log10(kd)))
                        exponent = int(np.floor(np.log10(kd)))
                        legend_label = fr"$K_D = {mantissa:.2f} \times 10^{{{exponent}}}$"
                    else:
                        legend_label = file
                        
                kon_value = kon if kon else 1
                all_kon.append(kon_value)

                print(f"kon_value extracted: {kon_value}")

                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        line, = plt.plot(data[:, 0], data[:, idx], label=legend_label)
                        line.set_color(get_color_for_kon(kon_value))
                        all_lines.append(line)
                        all_labels.append(legend_label)
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    sorted_indices = np.argsort(all_kon)
    all_lines_sorted = [all_lines[i] for i in sorted_indices]
    all_labels_sorted = [all_labels[i] for i in sorted_indices]

    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("CaMKII_open")
    plt.gca().set_facecolor('lightgrey')
    plt.grid(True)
    plt.tight_layout()

    plt.legend(all_lines_sorted, all_labels_sorted, title="Simulation runs with varying ($K_D$)", loc="lower right")

    output_png_filepath = os.path.join(target_folder, "all_variables_plot.png")
    plt.savefig(output_png_filepath, dpi=500)
    plt.show()
    print(f"Your combined plot has been saved as {output_png_filepath}")

if __name__ == "__main__":
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]
    selected_param_input = input("Enter parameter names to use in the legend (from the CSVs), separated by commas (or press Enter to skip): ")
    selected_param_names = [p.strip() for p in selected_param_input.split(",") if p.strip()]

    plot_multiple_gdat(target_folder, selected_variables, selected_param_names)
