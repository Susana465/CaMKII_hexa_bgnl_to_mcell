import os
import numpy as np
import matplotlib.pyplot as plt

def plot_target_file(target_file):
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
        plot_data(target_filepath)
    else:
        print(f"File '{target_file}' not found in any directory containing 'run_'")

def plot_data(target_filepath):
    # Load the data from the .gdat file
    data = np.loadtxt(fname=target_filepath)
    # Extract the header from the .gdat file
    with open(target_filepath, 'r') as f:
        header = f.readline().strip().split()[2:]
    
    plt.xlabel("Time")
    plt.ylabel("Molecule Count")
    plt.title("Molecules interacting throughout time")
    
    for i, column in enumerate(data.T[1:], start=1):
        plt.plot(data[:, 0], column, label=header[i-1])

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
    plot_target_file(target_file)
