import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def process_folder(folder_path, selected_variables=None):
    variable_data = {}
    time_values = None
    variables_determined = False

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                try:
                    data = np.loadtxt(fname=target_filepath)
                except Exception as e:
                    print(f"⚠️ Failed to read {file}: {e}")
                    continue

                if data.ndim == 1 or data.shape[1] < 2:
                    print(f"⚠️ Warning: {file} appears to have wrong format. Skipping.")
                    continue

                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.lstrip("#").split()
                    header = header[1:]  # skip 'time'

                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}

                if selected_variables is None and not variables_determined:
                    selected_variables = list(header_dict.keys())
                    variables_determined = True
                elif not variables_determined:
                    selected_variables = [var.lower() for var in selected_variables]
                    variables_determined = True

                if time_values is None:
                    time_values = data[:, 0]
                    print(f"⏰ Time values detected, shape: {time_values.shape}")

                for var_name in selected_variables:
                    if var_name in header_dict:
                        idx = header_dict[var_name]
                        variable_data.setdefault(var_name, []).append(data[:, idx])
                    else:
                        print(f"⚠️ Variable '{var_name}' not found in {file}. Skipping.")

    if not variable_data:
        print("❌ No variables were collected! Please check your selected variables and files.")
    else:
        print(f"✅ Variable data collected: {list(variable_data.keys())}")

    return variable_data, time_values

def plot_mean_from_gdat(wt_folder, mt_folder, selected_variables=None):
    wt_data, time_values = process_folder(wt_folder, selected_variables)
    mt_data, _ = process_folder(mt_folder, selected_variables)

    if not wt_data or not mt_data:
        print("❌ No data to plot. Please check your inputs.")
        return

    if selected_variables is None:
        selected_variables = list(wt_data.keys())

    color_palette = {
        "WT": "#66c2a5",
        "MT": "#fc8d62",
    }

    plt.figure(figsize=(10, 6))
    legend_handles = []
    used_y_positions = []

    def place_label(x_end, y_end, label_text, color):
        label_y = y_end
        min_sep = 2  # Minimum vertical separation

        def is_free(y_val):
            return all(abs(y_val - used) >= min_sep for used in used_y_positions)

        if not is_free(label_y):
            offset = min_sep
            while True:
                up = label_y + offset
                down = label_y - offset
                if is_free(up):
                    label_y = up
                    break
                elif is_free(down):
                    label_y = down
                    break
                offset += min_sep

        used_y_positions.append(label_y)

        plt.text(
            x_end + 0.5, label_y,
            label_text,
            fontsize=9.5,
            color=color,
            verticalalignment='center'
        )

    print("\n=== Final Mean Values at End of Simulation ===")

    for var_name in selected_variables:
        print(f"\n📊 Variable: {var_name}")

        # WT
        if var_name in wt_data:
            wt_arrays = np.stack(wt_data[var_name])
            wt_mean = np.mean(wt_arrays, axis=0)
            wt_std = np.std(wt_arrays, axis=0)

            print(f"    WT mean first 5 points: {wt_mean[:5]}")
            print(f"    ➡️ Final WT mean: {wt_mean[-1]:.3f}")

            color = color_palette["WT"]
            plt.plot(time_values, wt_mean, color=color, label=f"WT - {var_name}")
            plt.fill_between(time_values, wt_mean - wt_std, wt_mean + wt_std, color=color, alpha=0.3)
            legend_handles.append(Line2D([0], [0], color=color, lw=2, label=f"WT - {var_name}"))

            # Final point marker
            plt.plot(time_values[-1], wt_mean[-1], 'o', color=color)
            place_label(time_values[-1], wt_mean[-1], f"{wt_mean[-1]:.1f}", color)

        # MT
        if var_name in mt_data:
            mt_arrays = np.stack(mt_data[var_name])
            mt_mean = np.mean(mt_arrays, axis=0)
            mt_std = np.std(mt_arrays, axis=0)

            print(f"    MT mean first 5 points: {mt_mean[:5]}")
            print(f"    ➡️ Final MT mean: {mt_mean[-1]:.3f}")

            color = color_palette["MT"]
            plt.plot(time_values, mt_mean, color=color, label=f"MT - {var_name}")
            plt.fill_between(time_values, mt_mean - mt_std, mt_mean + mt_std, color=color, alpha=0.3)
            legend_handles.append(Line2D([0], [0], color=color, lw=2, label=f"MT - {var_name}"))

            # Final point marker
            plt.plot(time_values[-1], mt_mean[-1], 'o', color=color)
            place_label(time_values[-1], mt_mean[-1], f"{mt_mean[-1]:.1f}", color)

    plt.xlabel("Time (s)")
    plt.ylabel("Molecule Count")
    plt.gca().set_facecolor('whitesmoke')
    plt.grid(True)
    plt.tight_layout()
    plt.legend(handles=legend_handles, loc="lower right")

    output_png_filepath = os.path.join(wt_folder, "mean_variables_comparison.png")
    plt.savefig(output_png_filepath, dpi=500)
    plt.show()
    print(f"\n✅ Plot saved at {output_png_filepath}")

if __name__ == "__main__":
    print("=== Comparing WT and MT data ===")

    selected_variables_input = input("Enter variables to plot, separated by commas (or press Enter to plot all): ")
    selected_variables = [var.strip().lower() for var in selected_variables_input.split(",") if var.strip()]
    if not selected_variables:
        selected_variables = None

    WT_path = "D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/wetransfer_runs_wt-zip_2025-04-23_0856/WT"
    MT_path = "D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/runs_T286"

    plot_mean_from_gdat(WT_path, MT_path, selected_variables)
