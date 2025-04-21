import os
import numpy as np
from scipy.stats import shapiro

def load_final_values(folder_path, variable_name):
    final_values = []
    for root, dirs, files in os.walk(folder_path):  # Using os.walk for recursive search in subdirectories
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")  # Debug: Track files being processed

                # Read data
                data = np.loadtxt(target_filepath)
                if data.ndim == 1:
                    print(f"⚠️ Unexpected format in {file}. Skipping.")
                    continue

                # Read header and check if the variable exists
                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.split()[2:]  # Skip the first two columns (e.g., # time)

                print(f"Header in {file}: {header}")  # Debug: Show the header

                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}
                var_lower = variable_name.lower()

                if var_lower not in header_dict:
                    print(f"⚠️ Variable '{variable_name}' not found in {file}. Skipping.")
                    continue

                idx = header_dict[var_lower]
                final_val = data[-1, idx]  # Take the last data point for the variable
                final_values.append(final_val)

    return final_values


def check_normality(data, label):
    stat, p = shapiro(data)
    print(f"\n📊 Shapiro–Wilk test for {label}")
    print(f"  W = {stat:.4f}, p = {p:.4f}")
    if p > 0.05:
        print(f"  ✅ Data appears normally distributed.")
    else:
        print(f"  ❌ Data is NOT normally distributed.")


if __name__ == "__main__":
    variable = input("Enter variable to test (e.g. camkii_open): ").strip()

    wt_folder = input("Enter WT folder path: ").strip()
    mt_folder = input("Enter MT folder path: ").strip()

    wt_values = load_final_values(wt_folder, variable)
    mt_values = load_final_values(mt_folder, variable)

    print(f"\nWT: {len(wt_values)} values | MT: {len(mt_values)} values")

    if len(wt_values) < 3 or len(mt_values) < 3:
        print("⚠️ Not enough data to test normality. Need at least 3 data points per group.")
    else:
        check_normality(wt_values, "WT")
        check_normality(mt_values, "MT")
