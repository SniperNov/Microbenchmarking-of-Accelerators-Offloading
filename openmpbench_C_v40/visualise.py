import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.stats import linregress
import argparse
from scipy.optimize import curve_fit
import itertools


def read_file(filename):
    # Reading content from the specified output file and extracting data
    with open(filename, 'r') as file:
        content = file.read()
    return content

def plot_performance(benchmark_data, delays, job, IDA, graph):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delays) * 1.1, 100)

    for benchmark, data in benchmark_data.items():
        color = next(colors)
        slope, intercept, r_value, p_value, std_err = linregress(delays, data)
        analyse_dist(benchmark, job, slope, intercept, std_err)
        extended_predictions = intercept + slope * extended_x

        plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{benchmark} (y = {slope:.4f}x + {intercept:.4f})')
        plt.scatter(delays, data, color=color, edgecolor='black', s=50)

    if (graph==True):
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
        output_name = "Plots/" + job + "/arraybench_" + IDA + "_performance.png"
        plt.savefig(output_name)
        plt.show()
        print(f"Plot saved to {output_name}")


def plot_overhead(benchmark_overhead, delays, job, IDA, graph):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = itertools.cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delays) * 1.1, 100)

    for benchmark, data in benchmark_overhead.items():
        color = next(colors)       
        # Use UnivariateSpline for smoothing. s is a smoothing factor.
        spline = UnivariateSpline(delays, data, s=1)        
        # Plot the spline fit
        plt.plot(extended_x, spline(extended_x), color=color, linestyle='-', linewidth=2, label=f'{benchmark}')
        plt.scatter(delays, data, color=color, edgecolor='black', s=50)    
        # Determine the lower limit constant 'a' as the minimum of the smoothed data
        lower_limit_constant = np.min(spline(extended_x))
        # Plot the lower limit horizontal line
        plt.axhline(y=lower_limit_constant, color='gray', linestyle='--', label=f'Lower Limit (y = {lower_limit_constant:.2f})')

    if(graph==True):
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
        output_name = "Plots/" + job + "/arraybench_" + IDA + "_overhead.png"
        plt.savefig(output_name)
        plt.show()
        print(f"Plot saved to {output_name}")

def analyse_data(benchmark_name, job, data):
    file_name = "Analysis/" + job + "/data_" + benchmark_name + ".txt"
    with open(file_name, 'w') as data_file:
        for item in data:
            data_file.write(str(item) + ' ') 
        data_file.write('\n')

def analyse_dist(benchmark_name, job, gradient, interception, error):
    file_name = "Analysis/" + job + "/coe_" + benchmark_name + ".txt"
    with open(file_name, 'w') as coe_file:
        coe_file.write(f"{gradient} {interception} {error}\n")  # Using f-string for formatting

def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description='Parse and plot data from OpenMP benchmark output.')
    parser.add_argument('filename', type=str, help='Name of the output file to parse')
    parser.add_argument('IDA', type=str, default='1', help='Array Length')
    parser.add_argument('job',type=str,default='0',help='The Script JOB ID')

    args = parser.parse_args()
    content = read_file(args.filename)
    job = args.job
    IDA = args.IDA
    # Extract parameters
    param_pattern = r"Running OpenMP benchmark version \d+\.\d+\s+(\d+) thread\(s\)\s+(\d+) outer repetitions\s+([\d.]+) test time \(microseconds\)\s+(\d+) delay length \(iterations\)\s+([\d.]+) delay time \(microseconds\)"
    params = re.findall(param_pattern, content, re.DOTALL)

    delays = []
    benchmark_data = {}
    benchmark_overhead = {}

    if params:
        for i, (threads, outer_repetitions, test_time, delay_length, delay_time) in enumerate(params, start=1):
            delays.append(float(delay_time))
            # print(f"Run {i}: Threads: {threads}, Outer Repetitions: {outer_repetitions}, Test Time: {test_time} microseconds, Delay Length: {delay_length}, Delay Time: {delay_time} microseconds")
    else:
        print("Parameters not found in the file.")
        exit()

    benchmark_pattern = r"Computing (\w+) time using \d+ reps"
    benchmarks = re.findall(benchmark_pattern, content, re.DOTALL)
    if benchmarks:
        benchmark_data = {benchmark: [] for benchmark in benchmarks}
        benchmark_overhead = {benchmark: [] for benchmark in benchmarks if 'reference' not in benchmark}
        
        print("The Performance extracted:\n")
        print(benchmark_data)

        print("The Overheads extracted:\n")
        print(benchmark_overhead)
    else:
        print("Benchmarks not found in the file.")
        exit()

    # data_pattern = r"Sample_size\s+Mean\s+Median\s+Min\s+Max\s+StdDev\s+Outliers\n\s*\d+\s+([\d.]+)"
    data_pattern = r"mean time\s+=\s+([\d.]+)"
    all_data = re.findall(data_pattern, content, re.DOTALL)
    print("Performance mean time:\n")
    print(all_data)
    if all_data:
        for benchmark, mean_time in zip(benchmarks, all_data):
            benchmark_data[benchmark].append(float(mean_time))
        for benchmark, mean_times in benchmark_data.items():
            print(f"{benchmark}: {mean_times}")
            analyse_data(benchmark, job, mean_times)
    else:
        print("Data not found in the file.")
        exit()    

    overhead_pattern = r"overhead\s+=\s+(-?[\d.]+)"
    all_overhead = re.findall(overhead_pattern, content, re.DOTALL)
    print("Overheads:\n")
    print(all_overhead)
    benchmark_filtered = [item for item in benchmarks if 'reference' not in item]

    if all_overhead:
        for benchmark, overhead in zip(benchmark_filtered, all_overhead):
            benchmark_overhead[benchmark].append(float(overhead))
        for benchmark, overheads in benchmark_overhead.items():
            print(f"{benchmark}: {overheads}")
    else:
        print("Overhead not found in the file.")
        exit()        
    

    plot_performance(benchmark_data, delays, job, IDA, True)
    plot_overhead(benchmark_overhead, delays, job, IDA, True)


if __name__ == "__main__":
    main()
