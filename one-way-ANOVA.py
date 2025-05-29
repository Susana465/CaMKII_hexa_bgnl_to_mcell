import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statannotations.Annotator import Annotator

"""
This script performs statistical analysis on the final values of a specified molecule extracted from `.gdat` files
across multiple experimental groups. It uses one-way ANOVA to assess whether there are significant differences
between the groups, and generates a visualization with optional post-hoc significance annotations.

1. Prompts the user for a molecule name (e.g., "camkii_open", found in .gdat) to analyze.
2. Defines paths to directories containing `.gdat` simulation output files for multiple groups (e.g., WT, mutants).
3. For each group:
   - Recursively scans for `.gdat` files.
   - Loads the final value of the specified variable from each file.
4. Aggregates the final values and runs a one-way ANOVA test to compare group means.
5. If the ANOVA is significant (p < 0.05), performs Tukey’s HSD post hoc test to determine which group pairs differ.
6. Visualizes the data using a boxplot with:
   - Jittered data points.
   - Mean indicators.
   - Statistical significance stars (if applicable).

Output:
- Console output of ANOVA results and Tukey's HSD table (if applicable).
- A matplotlib plot displaying group comparisons with statistical annotations.

Dependencies:
- numpy, pandas, seaborn, matplotlib, scipy, statsmodels, statannotations
"""


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

    # Grid lines
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.5)

    # Display mean lines
    means = df.groupby('group')[variable_name].mean()
    for i, group in enumerate(group_paths.keys()):
        x_pos = i
        ax.plot([x_pos - 0.4, x_pos + 0.4], [means[group], means[group]], color='grey', linestyle='--', linewidth=2)

    # Tukey's post hoc if significant
    if p_val < 0.05:
        print("\nTukey's HSD Post Hoc Test:")
    
        tukey_res = pairwise_tukeyhsd(df[variable_name], df['group'])
        print(tukey_res.summary())  # Shows the summary of Tukey's HSD test

        # Extract pairs and p-values from Tukey's HSD result
        tukey_data = tukey_res._results_table.data[1:]  # Skip header row
        pairs = []
        pvals = []

        for row in tukey_data:
            group1, group2, meandiff, p_adj, lower, upper, reject = row
            pairs.append((group1, group2))
            pvals.append(p_adj)

        # Prepare Annotator for plotting the significance annotations
        annotator = Annotator(ax, pairs, data=df, x='group', y=variable_name)
        annotator.configure(test=None, text_format='star', loc='inside', verbose=0)
        annotator.set_pvalues_and_annotate(pvals)

    plt.title(variable_name)
    plt.ylabel("Final Molecule Count")
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== One-Way ANOVA on .gdat final values ===")
    variable_name = input("Enter the variable name (e.g., camkii_open): ").strip()

    wt_folder = "D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/wetransfer_runs_wt-zip_2025-04-23_0856/WT"        # <-- change this to your real WT path
    t286_folder = "D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/runs_T286"  # <-- change this to your real MT path
    nmdar_folder = "D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/thesis_results/NMDAR_MT_open_and_close_release"  # <-- change this to your real MT path

    group_paths = {
        "WT": wt_folder,
        "T286_MT": t286_folder,
        "NMDAR_CaMKII_MT": nmdar_folder
    }

    run_anova_analysis(group_paths, variable_name)
