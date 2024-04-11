# run this script in the command line with $ python plot_output.py
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

        # Load the data from the .gdat file
        data = np.loadtxt(fname=target_filepath)

        # Extract the header from the .gdat file
        with open(target_filepath, 'r') as f:
            header = f.readline().strip().split()[2:]

        # Plot the data
        plt.xlabel("Iterations")
        plt.ylabel("Molecule count")
        plt.title("Molecule counts through time")

        for i, column in enumerate(data.T[1:], start=1):
            plt.plot(data[:, 0], column, label=header[i-1])

        plt.legend()
        plt.show()

        # Save the .png file using the name of the .gdat file
        target_directory = os.path.dirname(target_filepath)
        # extract the filename without extension from the target_filepath
        target_filename_no_ext = os.path.splitext(os.path.basename(target_filepath))[0]
        target_png_filepath = os.path.join(target_directory, f"{target_filename_no_ext}.png")

        if os.path.exists(target_png_filepath):
            overwrite = input(f"A file already exists in this directory titled '{target_filename_no_ext}.png'. Do you want to proceed? This will overwrite the .png file (y/n) ")
            if overwrite.lower() == 'n':
                print("Your file was not overwritten.")
                return

        plt.savefig(target_png_filepath, dpi=500)

        # Notify the user about the saved .png file
        print(f"Your .gdat file has now been saved in {target_png_filepath}")
    else:
        print(f"File '{target_file}' not found in any directory containing 'run_'")

if __name__ == "__main__":
    target_file = input("Which .gdat file would you like to run? ")
    plot_target_file(target_file)