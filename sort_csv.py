import pandas as pd
import re

# Function to extract the decibel level
def extract_decibel(header):
    match = re.search(r"-(\d+)dB\.wav", header)
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # Return a large number if no match is found

# Load your CSV data into a DataFrame
# Replace 'your_csv_file.csv' with the actual file path
df = pd.read_csv('/Users/nptlinh/Desktop/BA-Code/gui_qt/results/transition/train.csv')

# Sort the DataFrame columns based on decibel level
sorted_columns = sorted(df.columns, key=extract_decibel)
df_sorted = df[sorted_columns]

# Now df_sorted is your DataFrame with columns sorted by decibel level
# You can save it to a new CSV or use it for plotting
# For example, to save to a new CSV:
df_sorted.to_csv('/Users/nptlinh/Desktop/BA-Code/gui_qt/results/transition/sorted_train.csv', index=False)