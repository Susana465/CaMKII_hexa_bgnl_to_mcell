import os
import numpy as np
import matplotlib.pyplot as plt

# this one goes thru all files
# avoid doing a full run of script as it will iterate and save a png for each folder, 
# only run if you want all figures at once

def plot_all_gdat_files(root_dir="."):
    # Function to search for all .gdat files within directories containing "run_"
    def find_gdat_files(root_dir):
        gdat_files = []
        for root, dirs, files in os.walk(root_dir):
            print(f"Inspecting directory: {root}")  # Debug: Print the directories being inspected
            for directory in dirs:
                if "run_" in directory:  # This condition is for directories that include 'run_'
                    directory_path = os.path.join(root, directory)
                    print(f"Searching in {directory_path}")  # Debug: Print the path being searched
                    for file in os.listdir(directory_path):
                        if file.endswith(".gdat"):
                            gdat_files.append(os.path.join(directory_path, file))
        return gdat_files

    # Get a list of all .gdat files in the directory
    gdat_files = find_gdat_files(root_dir)
    
    if gdat_files:
        for gdat_file in gdat_files:
            print(f"Processing file: {gdat_file}")

            # Load the data from the .gdat file
            data = np.loadtxt(fname=gdat_file)
            data_new = np.delete(data, 0, 1)  # Removing the first column if needed
            
            # Generate the plot
            plt.figure(figsize=(8, 6))
            plt.plot(data_new)
            plt.xlabel("Time(s)")
            plt.ylabel("Molecule count")
            plt.title(f"Molecule counts through time ({os.path.basename(gdat_file)})")
            
            # Save the plot as a PNG file using the .gdat filename (without extension)
            target_directory = os.path.dirname(gdat_file)
            target_filename_no_ext = os.path.splitext(os.path.basename(gdat_file))[0]
            output_png = os.path.join(target_directory, f"{target_filename_no_ext}.png")

            # Check if the PNG already exists
            if os.path.exists(output_png):
                print(f"Warning: {output_png} already exists.")
                user_input = input(f"Do you want to overwrite {output_png}? (y/n): ").strip().lower()
                
                # If the user answers 'n', skip saving this plot
                if user_input == 'n':
                    print(f"Skipping {output_png}.")
                    continue  # Skip saving this plot and move on to the next one
                # If the user answers anything else, including 'y', overwrite
                else:
                    print(f"Overwriting {output_png}.")

            plt.savefig(output_png, dpi=500)
            plt.close()  # Close the plot to avoid memory issues and unnecessary display

            print(f"Your plot has been saved as: {output_png}")
    else:
        print(f"No .gdat files found in any directory containing 'run_'")

if __name__ == "__main__":
    root_directory = "data_output"  # Start searching from the current directory or specify another
    plot_all_gdat_files(root_directory)
