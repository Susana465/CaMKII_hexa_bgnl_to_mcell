import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Parameters
num_runs = 8
max_time = 100  # seconds
time_points = np.linspace(0, max_time, 100)
np.random.seed(42)

# Define kon and koff values for each run in a dictionary (you can change the values as needed)
rate_constants = {
    "kon": [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10],  # Example kon values
    "koff": [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]  # Example koff values
}

# Formatter for scientific notation
fmt = mticker.LogFormatterSciNotation()

# Simulate cumulative molecule interactions for each run
data = []
for i in range(num_runs):
    steps = np.random.poisson(0.5, len(time_points))  # number of new interactions at each time
    cumulative = np.cumsum(steps)
    data.append(cumulative)

# Plot
plt.figure(figsize=(10, 6))
for i, y in enumerate(data):
    final_count = y[-1]
    exponent = int(np.floor(np.log10(final_count))) if final_count > 0 else 0
    
    # Access kon and koff values for the current run
    kon_value = rate_constants["kon"][i]
    koff_value = rate_constants["koff"][i]
    
    # Convert to scientific notation for legend
    kon_exponent = int(np.floor(np.log10(kon_value))) if kon_value > 0 else 0
    koff_exponent = int(np.floor(np.log10(koff_value))) if koff_value > 0 else 0
    
    # Construct the label with kon and koff values in scientific notation (LaTeX)
    label = fr"run {i+1} ($k_{{on}} = 10^{{{kon_exponent}}}$, $k_{{off}} = 10^{{{koff_exponent}}}$)"
    
    plt.step(time_points, y, where='post', label=label)

plt.title("Molecules Interacting Throughout Time")
plt.xlabel("Time (s)")
plt.ylabel("Molecule Count")
plt.legend(title="Simulation Runs")
plt.grid(True)
plt.tight_layout()
plt.show()
