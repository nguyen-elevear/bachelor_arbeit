import pandas as pd
import matplotlib.pyplot as plt
import math
import os
import numpy as np


def plot_box(filepaths):
    
    num_files = len(filepaths)

    # Determining the number of rows and columns for the subplot grid
    num_cols = int(math.ceil(math.sqrt(num_files)))
    num_rows = int(math.ceil(num_files / num_cols))

    # Creating a figure with subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(10 * num_cols, 6 * num_rows))
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Colors for different groups of columns
    colors = ['lightblue', 'lightgreen', 'lightcoral'] 
    # Iterating through each file and plotting
    for i, filepath in enumerate(filepaths):
        df = pd.read_csv(filepath).replace("",0)
        df = df.select_dtypes(include=[np.number])

        if 'comments' in df.columns:
            df = df.drop(columns=['comments'])
            
        ax = axes[i]
        boxplot = ax.boxplot(df, vert=True,
                     patch_artist=True)
        ax.set_title('Box Plot of ' + os.path.basename(filepath).split("_")[-1])
        ax.set_ylabel('Values')
        ax.tick_params(axis='x', rotation=45)  # Rotating the x-axis labels

        color_pattern = [colors[0], colors[0], colors[1], colors[1], colors[2], colors[2]]
        # Set colors for each group of columns
        for patch, color in zip(boxplot['boxes'], color_pattern[:len(df.columns)]):
            patch.set_facecolor(color)

        ax.set_xticklabels(df.columns, rotation=45, ha='right')
        ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.7)
    # Turn off any unused subplots
    for i in range(num_files, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()


