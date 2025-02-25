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

def plot_performance(benchmark_data, delays, job, MIDA, graph, machine):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delays) * 1.1, 100)
    directory = os.path.join("Analysis", machine, job)

    for benchmark, data in benchmark_data.items():
        color = next(colors)
        slope, intercept, r_value, p_value, std_err = linregress(delays, data)
        analyse_dist(benchmark, directory, slope, intercept, std_err, delays)
        extended_predictions = intercept + slope * extended_x

        plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{benchmark} (y = {slope:.4f}x + {intercept:.4f})')
        plt.scatter(delays, data, color=color, edgecolor='black', s=50)

    if (graph==True):
        plt.title(f'Performance, JOB={job}, Sampled in {MIDA} spacing on {machine}', fontsize=16, fontweight='bold')
        plt.xlabel('Delay Length (iterations))', fontsize=14)
        plt.ylabel('Mean execution time (microseconds)', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.tight_layout()
        output_name = "Plots/" + machine + "/"+ job + "/" + MIDA + "_performance.png"
        plt.savefig(output_name)
        plt.show()
        print(f"Plot saved to {output_name}")


def plot_overhead(benchmark_overhead, delays, job, MIDA, graph, machine):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delays) * 1.1, 100)

    for benchmark, data in benchmark_overhead.items():
        color = next(colors)
        slope, intercept, r_value, p_value, std_err = linregress(delays, data)
        extended_predictions = intercept + slope * extended_x

        plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{benchmark} (y = {slope:.4f}x + {intercept:.4f})')
        plt.scatter(delays, data, color=color, edgecolor='black', s=50)

    if(graph==True):
        plt.title(f'Overhead, JOB={job}, Sampled in {MIDA} spacing on {machine}', fontsize=16, fontweight='bold')
        plt.xlabel('Delay Length (iterations)', fontsize=14)
        plt.ylabel('Overhead (microseconds)', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.tight_layout()
        output_name = "Plots/" + machine + "/"+ job + "/" + MIDA + "_overhead.png"
        plt.savefig(output_name)
        plt.show()
        print(f"Plot saved to {output_name}")

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def analyse_data(benchmark_name, directory, data, delays):
    ensure_directory_exists(directory)
    file_name = os.path.join(directory, f"data_{benchmark_name}.txt")
    with open(file_name, 'a') as data_file:
        #If the file is empty then need to specify the column title.
        if os.path.getsize(file_name) == 0:
            #Convert delays list to a string with space-separated integers.
            delays_str = ' '.join(map(str, delays))
            data_file.write(f"{delays_str}\n")
        for item in data:
            data_file.write(str(item) + ' ')
        data_file.write('\n')

def analyse_dist(benchmark_name, directory, gradient, intercept, error, delays):
    ensure_directory_exists(directory)
    file_name = os.path.join(directory, f"coe_{benchmark_name}.txt")
    with open(file_name, 'a') as coe_file:
        #If the file is empty then need to specify the column title.
        # if os.path.getsize(file_name) == 0:
        #     #Convert delays list to a string with space-separated integers.
        #     delays_str = ' '.join(map(str, delays))
        #     coe_file.write(f"{delays_str}\n")
        coe_file.write(f"{gradient} {intercept} {error}\n") 

def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description='Parse and plot data from OpenMP benchmark output.')
    parser.add_argument('method',type=str,help='arraybench/schedbench/synchbench')
    parser.add_argument('filename', type=str, help='Name of the output file to parse')
    parser.add_argument('job',type=str,default='0',help='The Script JOB ID')
    parser.add_argument('IDA', type=str, default='1', help='Array Length')
    parser.add_argument('machine', type=str, default='Unknow', help='GPU machine')

    args = parser.parse_args()
    content = read_file(args.filename)
    job = args.job
    IDA = args.IDA
    method = args.method
    machine = args.machine
    directory = os.path.join("Analysis", machine, job)
    # Extract parameters
    param_pattern = r"Running OpenMP benchmark version \d+\.\d+\s+(\d+) thread\(s\)\s+(\d+) outer repetitions\s+([\d.]+) test time \(microseconds\)\s+(\d+) delay length \(iterations\)\s+([\d.]+) delay time \(microseconds\)"
    params = re.findall(param_pattern, content, re.DOTALL)

    delays = []
    benchmark_data = {}
    benchmark_overhead = {}

    if params:
        for i, (threads, outer_repetitions, test_time, delay_length, delay_time) in enumerate(params, start=1):
            delays.append(int(delay_length))
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
            analyse_data(benchmark, directory, mean_times, delays)
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
    
    print(f'delay lengths are {delays}!\n')
    plot_performance(benchmark_data, delays, job, method+'_'+IDA, True, machine)
    plot_overhead(benchmark_overhead, delays, job, method+'_'+IDA, True, machine)


if __name__ == "__main__":
    main()
