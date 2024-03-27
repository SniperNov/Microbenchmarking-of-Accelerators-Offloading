import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import argparse

def read_file(filename):
    # Reading content from the specified output file and extracting data
    with open(filename, 'r') as file:
        content = file.read()
    return content

def plot_performance(benchmark_data, delay_times, plot_filename):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delay_times) * 1.1, 100)

    for benchmark, data in benchmark_data.items():
        color = next(colors)
        slope, intercept, r_value, p_value, std_err = linregress(delay_times, data)
        extended_predictions = intercept + slope * extended_x

        plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{benchmark} (y = {slope:.4f}x + {intercept:.4f})')
        plt.scatter(delay_times, data, color=color, edgecolor='black', s=50)

    plt.title('Microbenchmarking OpenMP Target Offloading', fontsize=16, fontweight='bold')
    plt.xlabel('Delay Time (microseconds)', fontsize=14)
    plt.ylabel('Mean execution time (microseconds)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.show()
    print(f"Plot saved to {plot_filename}")

def plot_overhead(benchmark_data, delay_times, plot_filename):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delay_times) * 1.1, 100)

    for benchmark, data in benchmark_data.items():
        color = next(colors)
        slope, intercept, r_value, p_value, std_err = linregress(delay_times, data)
        extended_predictions = intercept + slope * extended_x

        plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{benchmark} (y = {slope:.4f}x + {intercept:.4f})')
        plt.scatter(delay_times, data, color=color, edgecolor='black', s=50)

    plt.title('Microbenchmarking OpenMP Target Offloading', fontsize=16, fontweight='bold')
    plt.xlabel('Delay Time (microseconds)', fontsize=14)
    plt.ylabel('Overhead (microseconds)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.show()
    print(f"Plot saved to {plot_filename}")

def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description='Parse and plot data from OpenMP benchmark output.')
    parser.add_argument('filename', type=str, help='Name of the output file to parse')
    parser.add_argument('output_dir', type=str, default='Plots', help='Directory to save the plot')
    args = parser.parse_args()

    content = read_file(args.filename)

    # Extract parameters
    param_pattern = r"Running OpenMP benchmark version \d+\.\d+\s+(\d+) thread\(s\)\s+(\d+) outer repetitions\s+([\d.]+) test time \(microseconds\)\s+(\d+) delay length \(iterations\)\s+([\d.]+) delay time \(microseconds\)"
    params = re.findall(param_pattern, content, re.DOTALL)

    delay_times = []
    benchmark_data = {}
    benchmark_overhead = {}

    if params:
        for i, (threads, outer_repetitions, test_time, delay_length, delay_time) in enumerate(params, start=1):
            delay_times.append(float(delay_time))
            # print(f"Run {i}: Threads: {threads}, Outer Repetitions: {outer_repetitions}, Test Time: {test_time} microseconds, Delay Length: {delay_length}, Delay Time: {delay_time} microseconds")
    else:
        print("Parameters not found in the file.")
        exit()

    benchmark_pattern = r"Computing (\w+) time using \d+ reps"
    benchmarks = re.findall(benchmark_pattern, content, re.DOTALL)
    if benchmarks:
        benchmark_data = {benchmark: [] for benchmark in benchmarks}
        benchmark_overhead = {benchmark: [] for benchmark in benchmarks if 'reference' not in benchmark}
        
        print("The Performance extracted:\n" + benchmark_data)

        print("The Overheads extracted:\n" + benchmark_overhead)
    else:
        print("Benchmarks not found in the file.")
        exit()

    # data_pattern = r"Sample_size\s+Mean\s+Median\s+Min\s+Max\s+StdDev\s+Outliers\n\s*\d+\s+([\d.]+)"
    data_pattern = r"mean time\s+=\s+([\d.]+)"
    all_data = re.findall(data_pattern, content, re.DOTALL)
    print("Performance mean time: "+all_data)
    if all_data:
        for benchmark, mean_time in zip(benchmarks, all_data):
            benchmark_data[benchmark].append(float(mean_time))
        for benchmark, mean_times in benchmark_data.items():
            print(f"{benchmark}: {mean_times}")
    else:
        print("Data not found in the file.")
        exit()    

    overhead_pattern = r"overhead\s+=\s+([\d.]+)"
    all_overhead = re.findall(overhead_pattern, content, re.DOTALL)
    print("Overheads:" + all_overhead)
    benchmark_filtered = [item for item in benchmarks if 'reference' not in item]
    if all_overhead:
        for benchmark, overhead in zip(benchmark_filtered, all_overhead):
            benchmark_overhead[benchmark].append(float(overhead))
        for benchmark, overheads in benchmark_overhead.items():
            print(f"{benchmark}: {overheads}")
    else:
        print("Overhead not found in the file.")
        exit()        
    

    # Ensure the output directory exists
    plot_performance(benchmark_data, delay_times, args.output_dir+'_performance_plot.png')
    plot_overhead(benchmark_overhead, delay_times, args.output_dir+'_overhead_plot.png')


if __name__ == "__main__":
    main()
