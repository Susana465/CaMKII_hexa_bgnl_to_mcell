import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Parameters
num_runs = 8
max_time = 100  # seconds
time_points = np.linspace(0, max_time, 100)
np.random.seed(42)

# Formatter for scientific notation
fmt = mticker.LogFormatterSciNotation()

# Simulate cumulative molecule interactions for each run
data = []
for _ in range(num_runs):
    steps = np.random.poisson(0.5, len(time_points))  # number of new interactions at each time
    cumulative = np.cumsum(steps)
    data.append(cumulative)

# Plot
plt.figure(figsize=(10, 6))
for i, y in enumerate(data):
    final_count = y[-1]
    exponent = int(np.floor(np.log10(final_count))) if final_count > 0 else 0
    label = fr"run {i+1} ($10^{{{exponent}}}$ molecules)"
    plt.step(time_points, y, where='post', label=label)

plt.title("Molecules Interacting Throughout Time")
plt.xlabel("Time (s)")
plt.ylabel("Molecule Count")
plt.legend(title="Simulation Runs")
plt.grid(True)
plt.tight_layout()
plt.show()
