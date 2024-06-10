import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

def std_diagram(data_content, job, filename, method, delaylength, machine):
    # delaylength = np.concatenate((np.linspace(20,1020, num=99),np.linspace(4900,5000,num=50))) #bot-top
    # delaylength = np.linspace(20,50000,num=100) #linear
    # delaylength = np.logspace(np.log10(20), np.log10(50000), num=100) #logarithmic
    # delaylength = np.concatenate((np.linspace(20,1000, num=99),np.array([50000]))) #booooot-top
    # delaylength = np.concatenate((np.array([20]),np.linspace(49020,50000, num=99))) #bot-tooooop
    # delaylength = delaylength[::-1]
    # f, (ax, ax2) = plt.subplots(1, 2, sharey=True, facecolor='w')
    # Convert delaylength to numeric values and sort them along with std
    delaylength_numeric = list(map(int, delaylength))
    sorted_indices = np.argsort(delaylength_numeric)
    sorted_delaylength = [delaylength[i] for i in sorted_indices]

    # Compute standard deviation for each data set and sort
    std = [np.std(data) for data in data_content]
    sorted_std = [std[i] for i in sorted_indices]

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(sorted_delaylength, sorted_std)
    plt.xticks(rotation=90, fontsize=8)  # Reduce font size by half (assuming default is 12 or 10)
    plt.xlabel('Delay Length')
    plt.ylabel('Standard Deviation')
    plt.title('Standard Deviation by Sorted Delay Length')
    plt.tight_layout()  # Adjust layout to make room for rotated x-ticks
    
    # ax.plot(delaylength, std)
    # ax2.plot(delaylength, std)

    # ax.set_xlim(0, 40)
    # ax2.set_xlim(49000, 50020)

    # ax.spines['right'].set_visible(False)
    # ax2.spines['left'].set_visible(False)
    # ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')
    # ax2.yaxis.tick_right()

    # d = .015  # how big to make the diagonal lines in axes coordinates
    # # arguments to pass plot, just so we don't keep repeating them
    # kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    # ax.plot((1-d, 1+d), (-d, +d), **kwargs)
    # ax.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

    plt.title(f'Change of standard deviation on {machine} of 100 dist, sampled by {method}, job={job}')
    plt.xlabel('Delay length (microsecond)')
    plt.ylabel('Standard Deviation')
    # ax.set_ylabel('Standard Deviation')
    # f.suptitle('Change of std of 100 distributions composed by 1000 independent runs')
    # ax.set_xlabel('Delay length (microsecond)')
    # ax2.set_xlabel('Delay length (microsecond)')


    plt.savefig(f"Analysis/{machine}/{job}/std_{filename}_{method}.png")
    print(f"File has been saved to {machine}/{job}/std_{filename}_{method}.png")


def runs_dist(data_content, job, filename, method, delaylength, machine):
    new_centers = np.linspace(0, 100, num=len(delaylength))
    plt.figure(figsize=(12, 6))
    for data, center in zip(data_content, new_centers):
        # Standardize each dataset
        standardized_data = data - np.mean(data)  # Centering at 0
        # Shift data to the new center
        shifted_data = standardized_data + center
        
        # Plot the adjusted distribution
        sns.kdeplot(shifted_data, bw_adjust=0.5)
        

    plt.title(f'Frequency for 100 runs on {machine}, {method} spaced, job={job}')
    plt.xticks(ticks=range(len(delaylength)), labels=delaylength, rotation=90)
    plt.xlabel('Order been linear scaled')
    plt.ylabel('Frequency')
    # Save the graph
    plt.savefig(f"Analysis/{machine}/{job}/freq_{method}_{filename}.png")
    plt.show()
    print(f"File has been saved to {machine}/{job}/freq_{method}_{filename}.png")

def coe_dist(coe_content, job, filename, method, machine):
    # Extract slope and interception values
    slope = coe_content[:, 0]
    interception = coe_content[:, 1]
    # std_error = coe_content[:, 2]

    # Plot the distributions of slopes and interceptions with histograms
    slope_mean = np.mean(slope)
    slope_median = np.median(slope)
    slope_std_dev = np.std(slope)
    interception_mean = np.mean(interception)
    interception_median = np.median(interception)
    interception_std_dev = np.std(interception)

    # Box plot for slopes and interceptions
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), tight_layout=True)

    axs[0].text(0.05, 0.95, f"Mean: {slope_mean:.6f}\nMedian: {slope_median:.6f}\nStd Dev: {slope_std_dev:.6f}",
            transform=axs[0].transAxes, va='top', ha='left', bbox=dict(boxstyle="round", facecolor='white', alpha=0.5))

    axs[1].text(0.05, 0.95, f"Mean: {interception_mean:.6f}\nMedian: {interception_median:.6f}\nStd Dev: {interception_std_dev:.6f}",
            transform=axs[1].transAxes, ha='right', va='top', bbox=dict(boxstyle="round",facecolor='white', alpha=0.5))

    # axs[0].violinplot(slope, vert=False, showmeans=True, showmedians=False, showextrema=False)
    sns.violinplot(y=slope, inner='quartile', ax=axs[0], color="lightgreen")
    # sns.pointplot(y=slope, ax=axs[0], color='red', scale=0.5, label='Mean')
    axs[0].set_title(f'Violin Plot of Slopes {method} spaced running on {machine}, job={job}')
    axs[0].set_ylabel('Slope Value')
    axs[0].grid(True) 

    # axs[1].violinplot(interception, vert=False, showmeans=True, showmedians=False, showextrema=False)
    sns.violinplot(y=interception,  inner='quartile', ax=axs[1], color="skyblue")
    # sns.pointplot(y=interception, ax=axs[0], color='red', scale=0.5, label='Mean')
    axs[1].set_title(f'Violin Plot of Intercepts {method} spaced running on {machine}, job={job}')
    axs[1].set_ylabel('Intercept Value')
    axs[1].grid(True) 

    plt.savefig(f"Analysis/{machine}/{job}/dist_{method}_{filename}.png")
    plt.show()
    print(f"File has been saved to {machine}/{job}/dist_{method}_{filename}.png")


def main():
    parser = argparse.ArgumentParser(description='Parse the multiple runs results and analysis the distribution.')
    parser.add_argument('data_filename', type=str, help='Name of the data file to parse')
    parser.add_argument('coe_filename', type=str, help='Name of the coeficient to parse')
    parser.add_argument('job',type=str, help='The output diagrams directory')
    parser.add_argument('method',type=str, help='Descriptions',default='unspecified')
    parser.add_argument('machine',type=str, help='GPU model',default='unspecified')

    args = parser.parse_args()
    method = args.method
    machine = args.machine
    # Extract 'filename' from the input file name using string methods
    parts = args.data_filename.split('_')
    filename = '_'.join(parts[1:])[:-4]  # This joins all parts between 'data' and '.txt'
    print(filename)

    # Read the first line separately which is the 'delaylength'
    with open(args.data_filename, 'r') as file:
        delays = list(file.readline().strip().split())
    print(f'Analysing datasets ...... read delay lengths are {delays}\n')
    data_content = np.transpose(np.loadtxt(args.data_filename, skiprows=1))

    coe_content = np.loadtxt(args.coe_filename)
    std_diagram(data_content, args.job, filename, method, delays, machine)
    runs_dist(data_content, args.job, filename, method, delays, machine)
    coe_dist(coe_content, args.job, filename, method, machine)

if __name__ == "__main__":
    main()