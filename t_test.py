import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statannotations.Annotator import Annotator

def load_final_values(folder_path, variable_name):
    final_values = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                data = np.loadtxt(target_filepath)
                if data.ndim == 1:
                    continue  # Skip if bad file

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

def run_analysis(group_paths: dict, variable_name: str):
    """Takes a dict of group_name -> folder_path and a variable name, runs analysis & shows plot."""
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

    # Custom color palette
    custom_palette = {
        'WT': '#66c2a5',             # Greenish
        'T286_MT': '#fc8d62',         # Reddish
        'NMDAR_CaMKII_MT': '#8da0cb'  # Bluish
    }

    # font size for plotting
    plt.rcParams.update({'font.size': 12})

    # Create the figure
    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(data=df, x='group', y=variable_name, palette=custom_palette, showmeans=False)

    # Add individual data points
    sns.stripplot(data=df, x='group', y=variable_name, color='black', jitter=True, alpha=0.6, size=6)

    # Grid lines
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.5)

    # Add dashed line for the means
    means = df.groupby('group')[variable_name].mean()
    for i, group in enumerate(group_paths.keys()):
        x_pos = i
        ax.plot([x_pos - 0.4, x_pos + 0.4], [means[group], means[group]], color='grey', linestyle='--', linewidth=2)

    # Statistical testing
    group_names = list(group_paths.keys())
    if len(group_names) == 2:
        # T-test
        group1_vals = df[df['group'] == group_names[0]][variable_name]
        group2_vals = df[df['group'] == group_names[1]][variable_name]
        stat, p_val = stats.ttest_ind(group1_vals, group2_vals)
        print(f"\nT-test between {group_names[0]} and {group_names[1]}: t={stat:.3f}, p={p_val:.3e}")

        pairs = [(group_names[0], group_names[1])]
        pvalues = [p_val]

        annotator = Annotator(ax, pairs, data=df, x='group', y=variable_name)
        annotator.configure(test=None, text_format='star', loc='inside', verbose=0)
        annotator.set_pvalues_and_annotate(pvalues)

    else:
        # ANOVA
        grouped_data = [df[df['group'] == g][variable_name] for g in group_names]
        f_stat, p_val = stats.f_oneway(*grouped_data)
        print(f"\nANOVA F-statistic: {f_stat:.3f}, p-value: {p_val:.3e}")

        if p_val < 0.05:
            print("\nTukey's HSD Post Hoc Test:")
            tukey_res = pairwise_tukeyhsd(df[variable_name], df['group'])
            print(tukey_res.summary())

            # Extract pairs and p-values
            tukey_data = tukey_res._results_table.data[1:]
            pairs = []
            pvals = []
            for row in tukey_data:
                group1, group2, meandiff, p_adj, lower, upper, reject = row
                pairs.append((group1, group2))
                pvals.append(p_adj)

            annotator = Annotator(ax, pairs, data=df, x='group', y=variable_name)
            annotator.configure(test=None, text_format='star', loc='inside', verbose=0)
            annotator.set_pvalues_and_annotate(pvals)

    plt.title(variable_name)
    plt.ylabel("Final Molecule Count")
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== T-test or ANOVA on .gdat final values ===")
    variable_name = input("Enter the variable name (e.g., camkii_open): ").strip()

    # Ask user for number of groups
    n_groups = int(input("Enter the number of groups (2 for T-test, 3+ for ANOVA): ").strip())

    group_paths = {}
    for i in range(n_groups):
        group_name = input(f"Enter the name for group {i+1}: ").strip()
        folder_path = input(f"Enter the folder path for {group_name}: ").strip()
        group_paths[group_name] = folder_path

    run_analysis(group_paths, variable_name)
