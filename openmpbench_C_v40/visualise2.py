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

def remove_outliers_iqr(data, delays, switch):
    if switch is 0:
        return data,delays
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    
    # Define the acceptable range for non-outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter data and corresponding delays
    filtered_data = [d for d, delay in zip(data, delays) if lower_bound <= d <= upper_bound]
    filtered_delays = [delay for d, delay in zip(data, delays) if lower_bound <= d <= upper_bound]
    
    return filtered_data, filtered_delays

def plot_performance(*datasets, tag, delays, job, MIDA, graph, machine):
    # Plotting performance based on extracted data
    plt.figure(figsize=(10, 6))
    colors = iter(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
    extended_x = np.linspace(0, max(delays) * 1.1, 100)
    directory = os.path.join("Analysis", machine, job)

    all_y_values = []

    for dataset in datasets:
        for label, data in dataset.items():
            filtered_data, filtered_delays = remove_outliers_iqr(data, delays,0)

            color = next(colors)
            slope, intercept, r_value, p_value, std_err = linregress(filtered_delays, filtered_data)
            analyse_dist(label, directory, slope, intercept, std_err, filtered_delays)
            extended_predictions = intercept + slope * extended_x

            plt.plot(extended_x, extended_predictions, color=color, linestyle='-', linewidth=2, label=f'{label} (y = {slope:.4f}x + {intercept:.4f})')
            plt.scatter(filtered_delays, filtered_data, color=color, edgecolor='black', s=50)
            all_y_values.extend(data)

    # Debugging output to check if negative values exist
    if graph:
        plt.title(f'Performance, JOB={job}, Sampled in {MIDA} spacing on {machine}', fontsize=16, fontweight='bold')
        plt.xlabel('Delay Length (iterations)', fontsize=14)
        plt.ylabel('Execution time (microseconds)', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.xlim(left=0)
        

        plt.tight_layout()
        output_name = os.path.join("Plots", machine, job, f"{tag}_{MIDA}_performance.png")
        os.makedirs(os.path.dirname(output_name), exist_ok=True)
        plt.savefig(output_name)
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

    # benchmark_pattern = r"Computing (\w+) time using \d+ reps"
    # benchmarks = re.findall(benchmark_pattern, content, re.DOTALL)
    # if benchmarks:
    #     benchmark_data = {benchmark: [] for benchmark in benchmarks}
    #     benchmark_overhead = {benchmark: [] for benchmark in benchmarks if 'reference' not in benchmark}
    reference_pattern = r"reference time mean time\s+=\s+([\d.]+)"
    all_pattern = r"testall mean time\s+=\s+([\d.]+)"
    observed_pattern = r"test1 mean time\s+=\s+([\d.]+)"
    expected_pattern = r"testall overhead\s+=\s+(-?[\d.]+)"

    reference_data = re.findall(reference_pattern, content)
    all_data = re.findall(all_pattern, content)
    observed_data = re.findall(observed_pattern, content)
    expected_data = re.findall(expected_pattern, content)

    if not observed_data or not expected_data or not reference_data or not all_data:
        print("Required data not found in the file.")
        exit()
    
    reference_data = [float(x) for x in reference_data]
    all_data = [float(x) for x in all_data]
    observed_data = [float(x) for x in observed_data]
    expected_data = [float(x) for x in expected_data]

    reference_dict = {"test2_measured": reference_data}
    all_dict = {"test1and2_measured": all_data}
    observed_dict = {"test1_measured": observed_data}
    expected_dict = {"test1_subtracted": expected_data}

    # Analyzing data and plotting
    analyse_data("test2_measured", directory, reference_data, delays)
    analyse_data("test1and2_measured", directory, all_data, delays)
    analyse_data("test1_measured", directory, observed_data, delays)
    analyse_data("test1_subtracted", directory, expected_data, delays)

    plot_performance(reference_dict, all_dict, tag='refall',delays=delays, job=job, MIDA=method + '_' + IDA, graph=True, machine=machine)
    plot_performance(observed_dict, expected_dict, tag='func1', delays=delays, job=job, MIDA=method + '_' + IDA, graph=True, machine=machine)


if __name__ == "__main__":
    main()
