# This script is to be run in command line as $ python plot_output.py
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

        data = np.loadtxt(fname=target_filepath)
        data_new = np.delete(data, 0, 1)

        # Call the plot function
        plot_data(data_new, target_filepath)
    else:
        print(f"File '{target_file}' not found in any directory containing 'run_'")

def plot_data(data, target_filepath):
    plt.xlabel("Iterations")
    plt.ylabel("Molecule count")
    plt.title("Molecule counts through time")

    plt.plot(data)

    # Save the .png file using the name of the .gdat file
    target_directory = os.path.dirname(target_filepath)
    # extract the filename without extension from the target_filepath
    target_filename_no_ext = os.path.splitext(os.path.basename(target_filepath))[0]
    # use target_filename_no_ext to save the .png file using the same filename as the .gdat file but with a .png extension
    plt.savefig(os.path.join(target_directory, f"{target_filename_no_ext}.png"), dpi=500)
    plt.show()
    # Notify the user about the saved .png file
    print(f"Your plot has now been saved in {os.path.join(target_directory, f'{target_filename_no_ext}.png')}")

if __name__ == "__main__":
    target_file = input("Which .gdat file would you like to plot? ")
    plot_target_file(target_file)
