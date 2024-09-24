import os
import numpy as np
import matplotlib.pyplot as plt

def plot_target_file(target_file, selected_variables=None):
    # Function to search for the target file within directories containing "run_"
    def find_target_file(root_dir, target_filename):
        for root, dirs, files in os.walk(root_dir):
            for directory in dirs:
                if "run_" in directory:
                    target_filepath = os.path.join(root, directory, target_filename)
                    if os.path.isfile(target_filepath):
                        return target_filepath
        return None

    # Search for the target file within the current directory "."
    target_filepath = find_target_file(".", target_file)

    if target_filepath is not None:
        print("Using file:", target_filepath)
        # Call the plot function
        plot_data(target_filepath, selected_variables)
    else:
        print(f"File '{target_file}' not found in any directory containing 'run_'")

def plot_data(target_filepath, selected_variables=None):
    # Load the data from the .gdat file
    data = np.loadtxt(fname=target_filepath)
    # Extract the header from the .gdat file
    with open(target_filepath, 'r') as f:
        header = f.readline().strip().split()[2:]
    
    # Create a dictionary to map variable names to their column indices
    header_dict = {var_name: idx+1 for idx, var_name in enumerate(header)}
    print(header_dict)

    # If specific variables are selected, use them, otherwise plot all
    if selected_variables is None:
        selected_variables = header  # Plot all variables
    
    plt.xlabel("Time(s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules interacting throughout time")
    
    for var_name in selected_variables:
        if var_name in header_dict:
            idx = header_dict[var_name]
            plt.plot(data[:, 0], data[:, idx], label=var_name)
        else:
            print(f"Variable '{var_name}' not found in data header")

    #for i, column in enumerate(data.T[1:], start=1):
    #    plt.plot(data[:, 0], column, label=header[i-1])

    plt.legend()

    # Save the plot as a PNG file
    target_directory = os.path.dirname(target_filepath)
    target_filename_no_ext = os.path.splitext(os.path.basename(target_filepath))[0]
    target_png_filepath = os.path.join(target_directory, f"{target_filename_no_ext}.png")
    plt.savefig(target_png_filepath, dpi=500)

    plt.show()
    print(f"Your plot has been saved as {target_png_filepath}")

if __name__ == "__main__":
    target_file = input("Which .gdat file would you like to plot? (add .gdat ending) ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]  # Clean whitespace
    plot_target_file(target_file, selected_variables)