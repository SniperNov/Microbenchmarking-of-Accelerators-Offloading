import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

def runs_dist(data_content, job, filename, method):
    # Plot histograms for each column
    fig, ax = plt.subplots(figsize=(20, 10))
    max_height = 0  # To store the max height of histograms for positioning text
    all_means = []

    data_range = [np.min(np.hstack(data_content)), np.max(np.hstack(data_content))]
    q25, q75 = np.percentile(np.hstack(data_content), [25, 75])
    bin_width = 2 * (q75 - q25) * len(np.hstack(data_content)) ** (-1/3)
    bins = int((data_range[1] - data_range[0]) / bin_width)

    for i, column in enumerate(data_content):
        counts, bins, patches = ax.hist(column, bins=bins, density=True, alpha=0.5, label=f'#{i+1}')
        tip = max(counts)
        if (tip > max_height):
            max_height = tip
        mean = np.mean(column)
        all_means.append(mean)
        median = np.median(column)
        std_dev = np.std(column)
        stats_text = f"#{i+1}:\nMean {mean:.2f}\nMedian {median:.2f}\nStd {std_dev:.2f}"
        # Position the stats text beside each histogram
        x_pos = mean + std_dev
        y_pos = tip * 1.1  # Adjust y position based on max histogram height
        ax.text(x_pos, y_pos, stats_text, verticalalignment='top', horizontalalignment='left', 
                bbox=dict(boxstyle="round", alpha=0.1, facecolor='white'))

    # Set the y-axis limit to ensure space for text
    ax.set_ylim(0, max_height * 1.15)  # Increase by 40% of the max height
    
    # Adjust the x-axis limit to ensure space for text annotations
    ax.set_xlim(min(all_means)*0.8, max(all_means) * 1.2) 

    # Set labels and title
    ax.set_xlabel('Performance (microseconds)')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Frequency diagram for 100 runs using {method} spcaed samples')
    ax.legend()
    
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
    axs[0].set_title('Violin Plot of Slopes - Samples spaced in Linear')
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

    runs_dist(data_content, args.job, filename, method)
    coe_dist(coe_content, args.job, filename, method)

if __name__ == "__main__":
    main()