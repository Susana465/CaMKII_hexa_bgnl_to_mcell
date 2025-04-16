import os
import numpy as np
import matplotlib.pyplot as plt

def plot_multiple_gdat(target_folder, selected_variables=None, variable_colors=None):
    """
    Reads and plots data from .gdat files in the specified folder.
    """
    plt.figure(figsize=(10, 6))

    already_plotted_vars = set()

    for root, dirs, files in os.walk(target_folder):
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

                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        color = variable_colors.get(var_name, None) if variable_colors else None
                        label = var_name if var_name not in already_plotted_vars else "_nolegend_"
                        line, = plt.plot(data[:, 0], data[:, idx], label=label)
                        if color:
                            line.set_color(color)
                        already_plotted_vars.add(var_name)
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.title("Simulation Output")
    plt.gca().set_facecolor('whitesmoke')
    plt.grid(True)
    plt.tight_layout()
    legend = plt.legend(loc="upper right")

    # Make legend lines thicker
    for line in legend.get_lines():
        line.set_linewidth(4)  # Thicker lines in legend for visibility
    
    output_png_filepath = os.path.join(target_folder, "all_variables_plot.png")
    plt.savefig(output_png_filepath, dpi=500)
    plt.show()
    print(f"Your combined plot has been saved as {output_png_filepath}")

if __name__ == "__main__":
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]

    # Define consistent colors here:
    variable_colors = {
        "cam_free": "gold",
        "cam_ca1": "darkkhaki",
        "cam_ca2": "olive",
        "cam_ca3": "olivedrab",
        "cam_ca4": "darkgreen",
        "camkii_cam_ca4": "violet",
        # Add more as needed...
    }

    plot_multiple_gdat(target_folder, selected_variables, variable_colors)
