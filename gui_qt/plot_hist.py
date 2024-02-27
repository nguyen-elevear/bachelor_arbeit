import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
import math
import numpy as np
import os
def plot_hist(filepath, start, end):
    df = pd.read_csv(filepath)

    file_basename = os.path.splitext(os.path.basename(filepath))[0]
    file_basename = file_basename.split("_")[-1]
    num_columns = len(df.columns[start:end])
    num_rows = int(np.ceil(np.sqrt(num_columns)))
    num_cols = num_rows
    bins = np.arange(-0.5, 11, 1)

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))

    # Flatten the axes array for easy iteration if it's 2D
    axes = axes.flatten()
    
    ylim = (0, 10)
    yticks = range(0, 11)

    plt.suptitle(file_basename, fontsize=16)
    # Iterate through the columns and create a subplot for each
    for i, column in enumerate(df.columns[start:end]):
        # Plot histogram on ith subplot
        axes[i].hist(df[column], bins=bins, edgecolor="black")
        axes[i].set_title(f'Histogram of {column}')
        axes[i].set_xlabel("Evaluation Score")
        axes[i].set_ylabel('Number of People')
        axes[i].set_xlim(-0.5, 10.5)
        axes[i].set_xticks(range(0, 11))
        axes[i].set_ylim(ylim)
        axes[i].set_yticks(yticks)

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    # Adjust layout so labels don't overlap
    plt.tight_layout()

    # Show the plot
    plt.show()

