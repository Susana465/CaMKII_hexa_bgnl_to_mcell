import os
import numpy as np
import matplotlib.pyplot as plt


# This plots all .gdat runs overlapped in one same png

def plot_multiple_gdat(target_folder, selected_variables=None):
    # Loop through all .gdat files in the folder
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                # Load the data from the .gdat file
                data = np.loadtxt(fname=target_filepath)

                # Extract the header from the .gdat file
                with open(target_filepath, 'r') as f:
                    header = f.readline().strip().split()[2:]  # Get header without the first two columns (time)
                
                # Create a dictionary to map variable names to their column indices
                header_dict = {var_name: idx+1 for idx, var_name in enumerate(header)}

                # If no specific variables are selected, plot all
                if selected_variables is None:
                    selected_variables = header  # Plot all variables

                # Plot selected variables
                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        plt.plot(data[:, 0], data[:, idx], label=f"{file} - {var_name}")
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Customize the plot
    plt.xlabel("Time(s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")
    plt.legend()

    # Save the plot as a PNG file
    output_png_filepath = os.path.join(target_folder, "all_variables_plot.png")
    plt.savefig(output_png_filepath, dpi=500)

    plt.show()
    print(f"Your combined plot has been saved as {output_png_filepath}")


if __name__ == "__main__":
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]  # Clean whitespace

    plot_multiple_gdat(target_folder, selected_variables)
