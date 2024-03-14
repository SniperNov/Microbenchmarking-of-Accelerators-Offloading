import os
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import argparse

# Setting up argument parser
parser = argparse.ArgumentParser(description='Parse and plot data from OpenMP benchmark output.')
parser.add_argument('filename', type=str, help='Name of the output file to parse')
args = parser.parse_args()

# Ensure the /Plots directory exists
plots_directory = 'Plots'
# os.makedirs(plots_directory, exist_ok=True)

# Reading content from the specified output file
with open(args.filename, 'r') as file:
    content = file.read()

# Regular expression patterns to extract parameter information
param_pattern = r"Running OpenMP benchmark version \d+\.\d+\s+(\d+) thread\(s\)\s+(\d+) outer repetitions\s+([\d.]+) test time \(microseconds\)\s+(\d+) delay length \(iterations\)\s+([\d.]+) delay time \(microseconds\)"
# Extracting parameters
params = re.findall(param_pattern, content, re.DOTALL)

#Xaixis
delay_times = []

if params:
    for i, (threads, outer_repetitions, test_time, delay_length, delay_time) in enumerate(params, start=1):
        delay_times.append(float(delay_time))
        print(f"Run {i}: Threads: {threads}, Outer Repetitions: {outer_repetitions}, Test Time: {test_time} microseconds, Delay Length: {delay_length}, Delay Time: {delay_time} microseconds")
else:
    print("Parameters not found in the file.")
    exit()

# Regular expression patterns to extract encountered benchmarks
benchmark_pattern = r"Computing (\w+) 1 time using \d+ reps"

# Extract benchmarks names
benchmarks = re.findall(benchmark_pattern, content, re.DOTALL)

if benchmarks:
    benchmark_data = {benchmark: [] for benchmark in benchmarks}
    print(benchmark_data)
else:
    print("Benchmarks not found in the file.")
    exit()

# Regular expression patterns to extract data
data_pattern = r"Sample_size\s+Mean\s+Median\s+Min\s+Max\s+StdDev\s+Outliers\n\s*\d+\s+([\d.]+)"
# Extract data
all_data = re.findall(data_pattern, content, re.DOTALL)
print(all_data)
if all_data:
    # Pair each benchmark with its corresponding mean time
    for benchmark, mean_time in zip(benchmarks, all_data):
        benchmark_data[benchmark].append(float(mean_time))
    # Print out the collected benchmark data
    for benchmark, mean_times in benchmark_data.items():
        print(f"{benchmark}: {mean_times}")
else:
    print("Data not found in the file.")
    exit()

# delay_times = [float(delay_time) * (2 ** i) for i in range(len(benchmark_data[next(iter(benchmark_data))]))]

# Plotting
plt.figure(figsize=(10, 6))
colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])  # More visually distinct colors
delay_times_np = np.array(delay_times).reshape(-1, 1)
for benchmark, data in benchmark_data.items():
    color = next(colors)
    data_np = np.array(data)
    # Linear regression
    reg = LinearRegression().fit(delay_times_np, data_np)
    predictions = reg.predict(delay_times_np)
    plt.plot(delay_times, predictions, color=color, linestyle='-', linewidth=2, marker='o', label=f'{benchmark} (y = {reg.coef_[0]:.4f}x + {reg.intercept_:.4f})')
    plt.scatter(delay_times, data, color=color, edgecolor='black', s=50)  # Actual data points

# Final plot adjustments
plt.title('Microbenchmarking OpenMP Target Offloading', fontsize=16, fontweight='bold')
plt.xlabel('Delay Time (microseconds)', fontsize=14)
plt.ylabel('Mean execution time (microseconds)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add grid
plt.minorticks_on()  # Add minor ticks
plt.tick_params(axis='both', which='major', labelsize=12)  # Adjust font size for ticks

# Set the beginning of x-axis and y-axis to 0
plt.xlim(left=0)
plt.ylim(bottom=0)

# Ensure layout is clean and labels don't get cut off
plt.tight_layout()

# Display the plot
plt.show()


# Saving the diagram
plot_filename = os.path.join(plots_directory, f'{os.path.basename(args.filename).split(".")[0]}_performance_plot.png')
plt.savefig(plot_filename)
print(f"Plot saved to {plot_filename}")
