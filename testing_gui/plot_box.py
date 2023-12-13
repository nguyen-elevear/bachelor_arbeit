import pandas as pd
import matplotlib.pyplot as plt
import math
import os


def plot_box(filepaths):
    
    num_files = len(filepaths)

    # Determining the number of rows and columns for the subplot grid
    num_cols = int(math.ceil(math.sqrt(num_files)))
    num_rows = int(math.ceil(num_files / num_cols))

    # Creating a figure with subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(10 * num_cols, 6 * num_rows))
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Iterating through each file and plotting
    for i, filepath in enumerate(filepaths):
        df = pd.read_csv(filepath).replace("",0)

        ax = axes[i]
        df.boxplot(ax=ax)
        ax.set_title('Box Plot of ' + os.path.basename(filepath))
        ax.set_ylabel('Values')
        ax.tick_params(axis='x', rotation=45)  # Rotating the x-axis labels

    # Turn off any unused subplots
    for i in range(num_files, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()

