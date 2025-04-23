import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

def load_final_values(folder_path, variable_name):
    final_values = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                data = np.loadtxt(target_filepath)
                if data.ndim == 1:
                    continue  # Skip malformed

                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.split()[2:]  # skip "# time"

                header_dict = {var.lower(): idx + 1 for idx, var in enumerate(header)}
                var_lower = variable_name.lower()

                if var_lower in header_dict:
                    idx = header_dict[var_lower]
                    final_val = data[-1, idx]
                    final_values.append(final_val)
    return final_values

def run_anova_analysis(group_paths: dict, variable_name: str):
    """Takes a dict of group_name -> folder_path and a variable name, runs ANOVA & shows plot"""
    all_data = []
    for group, path in group_paths.items():
        vals = load_final_values(path, variable_name)
        if len(vals) < 3:
            print(f"⚠️ Not enough data in {group}. Need at least 3 values.")
        for val in vals:
            all_data.append({"group": group, variable_name: val})

    df = pd.DataFrame(all_data)

    if df['group'].value_counts().min() < 3:
        print("❌ Cannot proceed. Each group must have at least 3 values.")
        return

    # ANOVA
    grouped_data = [df[df['group'] == g][variable_name] for g in group_paths.keys()]
    f_stat, p_val = stats.f_oneway(*grouped_data)
    print(f"\nANOVA F-statistic: {f_stat:.3f}, p-value: {p_val:.3e}")

    # font size for plotting
    plt.rcParams.update({'font.size': 12})

    # Boxplot
    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(data=df, x='group', y=variable_name, palette="Set2")
    
    # Add the individual data points
    sns.stripplot(data=df, x='group', y=variable_name, color='black', jitter=True, alpha=0.6, size=6)

    # Add grid lines with more frequency (minor and major)
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.minorticks_on()  # Enable minor ticks
    plt.grid(True, which='minor', linestyle=':', alpha=0.5)  # Minor grid lines

    # Display mean values as grey dashed lines across the entire width of each box
    means = df.groupby('group')[variable_name].mean()
    for i, group in enumerate(group_paths.keys()):
        # Get the x position of the group (to align with the boxplot)
        x_pos = i
        # Draw a grey dashed line for the mean across the full width of the boxplot
        ax.plot([x_pos - 0.4, x_pos + 0.4], [means[group], means[group]], color='grey', linestyle='--', linewidth=2)

    plt.title(variable_name)
    plt.ylabel("Final Molecule Count")
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== One-Way ANOVA on .gdat final values ===")
    variable_name = input("Enter the variable name (e.g., camkii_open): ").strip()

    wt_folder = input("Enter the WT folder path: ").strip()
    t286_folder = input("Enter the T286_mutant folder path: ").strip()
    nmdar_folder = input("Enter the NMDAR_CaMKII_MT folder path: ").strip()

    group_paths = {
        "WT": wt_folder,
        "T286_MT": t286_folder,
        "NMDAR_CaMKII_MT": nmdar_folder
    }

    run_anova_analysis(group_paths, variable_name)
