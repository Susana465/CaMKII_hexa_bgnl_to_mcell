import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Parameters
num_runs = 8
max_time = 100  # seconds
time_points = np.linspace(0, max_time, 100)
np.random.seed(42)

# Define kon and koff values for each run
rate_constants = {
    "kon": [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10],
    "koff": [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]
}

# Normalize kon values for colormap
kon_values = np.array(rate_constants["kon"])
norm = mcolors.LogNorm(vmin=kon_values.min(), vmax=kon_values.max())  # log-scale for better distribution
cmap = cm.get_cmap("Blues")  # choose your colormap

# Formatter for scientific notation
fmt = mticker.LogFormatterSciNotation()

# Simulate cumulative molecule interactions for each run
data = []
for i in range(num_runs):
    steps = np.random.poisson(0.5, len(time_points))  # number of new interactions at each time
    cumulative = np.cumsum(steps)
    data.append(cumulative)

# Plot and collect handles/labels for custom legend
plt.figure(figsize=(10, 6))
legend_entries = []

for i, y in enumerate(data):
    final_count = y[-1]
    kon_value = kon_values[i]
    koff_value = rate_constants["koff"][i]

    # Exponents for labeling
    kon_exp = int(np.floor(np.log10(kon_value))) if kon_value > 0 else 0
    koff_exp = int(np.floor(np.log10(koff_value))) if koff_value > 0 else 0

    label = fr"run {i+1} ($k_{{on}} = 10^{{{kon_exp}}}$, $k_{{off}} = 10^{{{koff_exp}}}$)"
    
    color = cmap(norm(kon_value))
    line, = plt.step(time_points, y, where='post', label=label, color=color)
    
    legend_entries.append((line, label, kon_value))

# Sort legend by kon descending (darker = higher kon)
legend_entries.sort(key=lambda x: x[2], reverse=True)
handles, labels, _ = zip(*legend_entries)

# Final plot touches
plt.title("Molecules Interacting Throughout Time")
plt.xlabel("Time (s)")
plt.ylabel("Molecule Count")
plt.grid(True)
plt.legend(handles, labels, title="Simulation Runs (sorted by $k_{on}$)", loc="upper left")
plt.tight_layout()
plt.show()

