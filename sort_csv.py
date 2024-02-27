import pandas as pd
import re

# Function to extract the decibel level
def extract_decibel(header):
    match = re.search(r"-(\d+)dB\.wav", header)
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # Return a large number if no match is found

df = pd.read_csv('/Users/nptlinh/Desktop/BA-Code/gui_qt/results/filter_pos/train.csv')

# Sort the DataFrame columns based on decibel level
sorted_columns = sorted(df.columns, key=extract_decibel)
df_sorted = df[sorted_columns]

df_sorted.to_csv('/Users/nptlinh/Desktop/BA-Code/gui_qt/results/filter_pos/sorted_train.csv', index=False)