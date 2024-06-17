import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
# import keyboard

def std_diagram(data_content, job, filename):
    # delaylength = np.concatenate((np.linspace(20,1020, num=99),np.linspace(4900,5000,num=50))) #bot-top
    # delaylength = np.linspace(20,50000,num=100) #linear
    delaylength = np.logspace(np.log10(20), np.log10(50000), num=100) #logarithmic
    # delaylength = np.concatenate((np.linspace(20,1000, num=99),np.array([50000]))) #booooot-top
    # delaylength = np.concatenate((np.array([20]),np.linspace(49020,50000, num=99))) #bot-tooooop

    # f, (ax, ax2) = plt.subplots(1, 2, sharey=True, facecolor='w')
    plt.figure(figsize=(12, 6))
    std=[]
    for data in data_content:
        std.append(np.std(data))
    plt.plot(delaylength, std)
    # plt.scatter(delaylength, std)
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

    plt.title(f'Change of std of 100 distributions composed by 1000 independent runs')
    plt.xlabel('Delay length (microsecond)')
    plt.ylabel('Standard Deviation')
    # ax.set_ylabel('Standard Deviation')
    # f.suptitle('Change of std of 100 distributions composed by 1000 independent runs')
    # ax.set_xlabel('Delay length (microsecond)')
    # ax2.set_xlabel('Delay length (microsecond)')


    plt.savefig(f"Analysis/{job}/std_{filename}.png")
    print(f"File has been saved to {job}/std_{filename}.png")


def runs_dist(data_content, job, filename, method):
    new_centers = np.linspace(0, 100, num=len(data_content))
    plt.figure(figsize=(12, 6))
    for data, center in zip(data_content, new_centers):
        # Standardize each dataset
        standardized_data = data - np.mean(data)  # Centering at 0
        # Shift data to the new center
        shifted_data = standardized_data + center
        
        # Plot the adjusted distribution
        sns.kdeplot(shifted_data, bw_adjust=0.5)

    plt.title(f'Frequency diagram for 100 runs using {method} spcaed samples')
    plt.xlabel('Order - linear spaced')
    plt.ylabel('Frequency')
    # Save the graph
    plt.savefig(f"Analysis/{job}/freq_{method}_{filename}.png")
    plt.show()
    print(f"File has been saved to {job}/freq_{method}_{filename}.png")

def coe_dist(coe_content, job, filename, method):
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
    axs[0].set_title(f'Violin Plot of Slopes - Samples spaced in {method}')
    axs[0].set_ylabel('Slope Value')
    axs[0].grid(True) 

    # axs[1].violinplot(interception, vert=False, showmeans=True, showmedians=False, showextrema=False)
    sns.violinplot(y=interception,  inner='quartile', ax=axs[1], color="skyblue")
    # sns.pointplot(y=interception, ax=axs[0], color='red', scale=0.5, label='Mean')
    axs[1].set_title(f'Violin Plot of Interceptions - Samples spaced in {method}')
    axs[1].set_ylabel('Interception Value')
    axs[1].grid(True) 

    plt.savefig(f"Analysis/{job}/dist_{method}_{filename}.png")
    plt.show()
    print(f"File has been saved to {job}/dist_{method}_{filename}.png")


def main():
    parser = argparse.ArgumentParser(description='Parse the multiple runs results and analysis the distribution.')
    parser.add_argument('data_filename', type=str, help='Name of the data file to parse')
    parser.add_argument('coe_filename', type=str, help='Name of the coeficient to parse')
    parser.add_argument('job',type=str, help='The output diagrams directory')
    parser.add_argument('method',type=str, help='Descriptions',default='unspecified')

    args = parser.parse_args()
    method = args.method
    # Extract 'filename' from the input file name using string methods
    parts = args.data_filename.split('_')
    filename = '_'.join(parts[1:])[:-4]  # This joins all parts between 'data' and '.txt'
    print(filename)


    data_content = np.transpose(np.loadtxt(args.data_filename))
    coe_content = np.loadtxt(args.coe_filename)
    std_diagram(data_content, args.job, filename)
    runs_dist(data_content, args.job, filename, method)
    coe_dist(coe_content, args.job, filename, method)

if __name__ == "__main__":
    main()