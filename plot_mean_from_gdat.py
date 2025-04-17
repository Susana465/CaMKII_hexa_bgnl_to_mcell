import os
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_from_gdat(target_folder, selected_variables=None, variable_colors=None):
    """
    Reads multiple .gdat files from a folder, computes mean and std for selected variables,
    and plots the average trace across simulations.
    """
    plt.figure(figsize=(10, 6))
    variable_data = {}  # Stores time-series data for each variable across files
    time_values = None

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

                if time_values is None:
                    time_values = data[:, 0]

                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        variable_data.setdefault(var_name, []).append(data[:, idx])
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")

    # Plot mean and standard deviation for each variable
    for var_name, all_arrays in variable_data.items():
        stacked = np.stack(all_arrays)
        mean_values = np.mean(stacked, axis=0)
        std_values = np.std(stacked, axis=0)

        color = variable_colors.get(var_name, None)
        label = var_name
        line = plt.plot(time_values, mean_values, label=label)[0]
        if color:
            line.set_color(color)

        # Optional: shaded area for ±1 std
        plt.fill_between(
            time_values,
            mean_values - std_values,
            mean_values + std_values,
            color=color or line.get_color(),
            alpha=0.3
        )

        # Final value marker and label
        x_end = time_values[-1]
        y_end = mean_values[-1]
        plt.plot(x_end, y_end, 'o', color=color or line.get_color())
        plt.text(
            x_end + 0.5, y_end,
            f"{y_end:.1f}",
            fontsize=9.5,
            color=color or line.get_color(),
            verticalalignment='center'
        )

    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.gca().set_facecolor('whitesmoke')
    plt.grid(True)
    plt.tight_layout()
    legend = plt.legend(loc="upper left")

    for line in legend.get_lines():
        line.set_linewidth(4)

    output_png_filepath = os.path.join(target_folder, "mean_variables_plot.png")
    plt.savefig(output_png_filepath, dpi=500)
    plt.show()
    print(f"Your mean trace plot has been saved as {output_png_filepath}")

if __name__ == "__main__":
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]

    # Define consistent colors for variables
    variable_colors = {
        "cam_free": "gold",
        "cam_ca1": "darkkhaki",
        "cam_ca2": "olive",
        "cam_ca3": "olivedrab",
        "cam_ca4": "darkgreen",
        "camkii_cam_ca4": "violet",
        "camkii_cam_unbound_open": "dodgerblue",
        "camkii_open": "saddlebrown",
        "nmdar_free": "deepskyblue",
        "nmdar_camkii_complex": "mediumblue",
        "camkii_t286p": "orangered",
        "camkii_t286p1_bound_nmdar": "hotpink",
        "camkii_cam_unbound_open_t286p1": "lightsalmon",
        "camkii_cam_ca4_t286p1_bound_nmdar": "mediumorchid",
        # Add more as needed...
    }

    plot_mean_from_gdat(target_folder, selected_variables, variable_colors)
