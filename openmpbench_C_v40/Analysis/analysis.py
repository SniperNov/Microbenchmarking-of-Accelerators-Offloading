import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import argparse


def runs_dist(data_content, job, filename):
    # Plot histograms for each column
    fig, ax = plt.subplots(figsize=(20, 10))
    n_bins = 50  # Adjust the number of bins for finer granularity
    max_height = 0  # To store the max height of histograms for positioning text
    all_means = []
    for i, column in enumerate(data_content):
        counts, bins, patches = ax.hist(column, bins=n_bins, density=True, alpha=0.5, label=f'#{i+1}')
        tip = max(counts)
        if (tip > max_height):
            max_height = tip
        mean = np.mean(column)
        all_means.append(mean)
        median = np.median(column)
        std_dev = np.std(column)
        stats_text = f"#{i+1}:\nMean {mean:.2f}\nMedian {median:.2f}\nStd {std_dev:.2f}"
        print
        # Position the stats text beside each histogram
        x_pos = mean + std_dev
        y_pos = tip * 1.1  # Adjust y position based on max histogram height
        ax.text(x_pos, y_pos, stats_text, verticalalignment='top', horizontalalignment='left', 
                bbox=dict(boxstyle="round", alpha=0.1, facecolor='white'))

    # Set the y-axis limit to ensure space for text
    ax.set_ylim(0, max_height * 1.15)  # Increase by 40% of the max height
    
    # Adjust the x-axis limit to ensure space for text annotations
    ax.set_xlim(min(all_means)*0.8, max(all_means) * 1.2) 
    # ax.set_xscale("")
    # Set labels and title
    ax.set_xlabel('Performance (microseconds)')
    ax.set_ylabel('Density')
    ax.set_title('Densities for 100 runs')
    ax.legend()
    
    # Save the graph
    plt.savefig(f"Analysis/{job}/density_log_{filename}.png")
    plt.show()
    print(f"File has been saved to {job}/density_log_{filename}.png")

def coe_dist(coe_content, job, filename):
    # Extract slope and interception values
    slope = coe_content[:, 0]
    interception = coe_content[:, 1]
    std_error = coe_content[:, 2]

    # Remove outliers based on standard error
    outliers_mask = np.abs(zscore(std_error)) > 1.96  # Using 95% confidence interval
    slope_filtered = slope[~outliers_mask]
    interception_filtered = interception[~outliers_mask]
    outliers_count = np.sum(outliers_mask)

    # Plot the distributions of slopes and interceptions with histograms
    slope_mean = np.mean(slope_filtered)
    slope_median = np.median(slope_filtered)
    slope_std_dev = np.std(slope_filtered)
    interception_mean = np.mean(interception_filtered)
    interception_median = np.median(interception_filtered)
    interception_std_dev = np.std(interception_filtered)

     # Box plot for slopes and interceptions
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), tight_layout=True)

    axs[0].text(0.95, 0.9, f"Mean: {slope_mean:.6f}\nMedian: {slope_median:.6f}\nStd Dev: {slope_std_dev:.6f}",
            transform=axs[0].transAxes, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))

    axs[1].text(0.95, 0.8, f"Mean: {interception_mean:.6f}\nMedian: {interception_median:.6f}\nStd Dev: {interception_std_dev:.6f}",
            transform=axs[1].transAxes, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))

    axs[0].boxplot(slope_filtered, notch=True, vert=True, patch_artist=True)
    axs[0].set_title('Box Plot of Slopes')
    axs[0].set_ylabel('Slope Value')

    axs[1].boxplot(interception_filtered, notch=True, vert=True, patch_artist=True)
    axs[1].set_title('Box Plot of Interceptions')
    axs[1].set_ylabel('Interception Value')

    plt.savefig(f"Analysis/{job}/distribution_log_{filename}.png")
    plt.show()
    print(f"File has been saved to {job}/distribution_log_{filename}.png")


def main():
    parser = argparse.ArgumentParser(description='Parse the multiple runs results and analysis the distribution.')
    parser.add_argument('data_filename', type=str, help='Name of the data file to parse')
    parser.add_argument('coe_filename', type=str, help='Name of the coeficient to parse')
    parser.add_argument('job',type=str, help='The output diagrams directory')

    args = parser.parse_args()
    # Extract 'filename' from the input file name using string methods
    parts = args.data_filename.split('_')
    filename = '_'.join(parts[1:])[:-4]  # This joins all parts between 'data' and '.txt'
    print(filename)


    data_content = np.transpose(np.loadtxt(args.data_filename))
    coe_content = np.loadtxt(args.coe_filename)

    runs_dist(data_content, args.job, filename)
    coe_dist(coe_content, args.job, filename)

if __name__ == "__main__":
    main()