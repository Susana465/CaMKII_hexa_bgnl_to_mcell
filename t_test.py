import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Function to load final values from .gdat files
def load_final_values(folder_path, variable_name):
    final_values = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                data = np.loadtxt(target_filepath)
                if data.ndim == 1:
                    continue  # Skip if the data format is unexpected
                
                # Read header to find the index of the variable
                with open(target_filepath, 'r') as f:
                    first_line = f.readline().strip()
                    header = first_line.split()[2:]  # Skip the "# time" column
                
                header_dict = {var_name.lower(): idx + 1 for idx, var_name in enumerate(header)}
                var_lower = variable_name.lower()

                if var_lower in header_dict:
                    idx = header_dict[var_lower]
                    final_val = data[-1, idx]  # Use the last data point
                    final_values.append(final_val)
    
    return final_values

# Function to perform a T-test between WT and MT
def perform_ttest(wt_values, mt_values):
    stat, p_value = ttest_ind(wt_values, mt_values)
    print(f"T-test result: t-statistic = {stat:.3f}, p-value = {p_value:.3f}")
    return p_value

# Function to get color from seaborn Set2 palette
def get_color_from_palette(variable_name, palette):
    color_idx = abs(hash(variable_name.lower())) % len(palette)
    return palette[color_idx]

# Function to plot bar plot for the chosen variable with error bars
def plot_bar_chart(wt_values, mt_values, variable_name):
    # Get color from Set2 palette
    palette = sns.color_palette("Set2", n_colors=20)  # You can adjust n_colors if needed
    color = get_color_from_palette(variable_name, palette)
    
    # Calculate means and SEMs
    mean_wt = np.mean(wt_values)
    std_wt = np.std(wt_values)
    sem_wt = std_wt / np.sqrt(len(wt_values))
    
    mean_mt = np.mean(mt_values)
    std_mt = np.std(mt_values)
    sem_mt = std_mt / np.sqrt(len(mt_values))
    
    # Create bar plot with error bars
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Bar positions
    bar_width = 0.4
    index = np.arange(2)  # two bars, one for MT and one for WT
    
    # Bars
    bars = ax.bar(index, [mean_wt, mean_mt], bar_width, yerr=[sem_wt, sem_mt], color=[color, color], capsize=5, label=["WT", "MT"])
    
    # Set axis labels and title
    ax.set_xlabel("Wild type vs T286 phospho-abolished mutant")
    ax.set_ylabel("Molecule Count")
    ax.set_title(f"Comparison of total {variable_name}: WT vs MT")
    
    # Set x-axis ticks and labels
    ax.set_xticks(index)
    ax.set_xticklabels(["WT", "MT"])
    
    # Show the mean values on top of the bars with SEM in parentheses
    for bar, mean, sem in zip(bars, [mean_wt, mean_mt], [sem_wt, sem_mt]):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 2, f"{yval:.2f} (SEM: {sem:.2f})", ha="center", va="bottom", fontsize=10)
    
    # Perform the T-test and show the p-value on the plot
    p_value = perform_ttest(wt_values, mt_values)
    ax.text(0.5, max(mean_wt, mean_mt) + 0.5, f"P-value: {p_value:.3f}", ha="center", va="bottom", fontsize=12, color="black")
    
    plt.tight_layout()
    plt.show()

# Main function to bring everything together
if __name__ == "__main__":
    # Input
    variable_name = input("Enter the variable name (e.g. camkii_open): ").strip()
    wt_folder = input("Enter the WT folder path: ").strip()
    mt_folder = input("Enter the MT folder path: ").strip()
    
    # Load values for WT and MT
    wt_values = load_final_values(wt_folder, variable_name)
    mt_values = load_final_values(mt_folder, variable_name)
    
    # Check if we have enough data
    if len(wt_values) < 3 or len(mt_values) < 3:
        print("⚠️ Not enough data to perform the analysis. Need at least 3 data points per group.")
    else:
        # Plot Bar Chart with error bars and p-value
        plot_bar_chart(wt_values, mt_values, variable_name)
