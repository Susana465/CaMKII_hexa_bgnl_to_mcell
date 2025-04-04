import os
import numpy as np
import matplotlib.pyplot as plt

def plot_multiple_gdat(target_folder, selected_variables=None):
    """
    Reads and plots data from .gdat files in the specified folder, 
    can iteratively go through multiple subfolders.
    
    Parameters:
    target_folder (str): Path to the folder containing .gdat files.
    selected_variables (list of str, optional): Variables to plot. If None, all variables are plotted.
    """
    plt.figure(figsize=(8, 5))  # Adjust figure size
    
    for root, dirs, files in os.walk(target_folder):
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

                # Plot each selected variable
                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        plt.plot(data[:, 0], data[:, idx], label=f"{file} - {var_name}")
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Customize plot
    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
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

    plot_multiple_gdat(target_folder, selected_variables)
