import os
import csv


# Function to read existing header
def read_header(file_path):
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            return next(reader, None)
    return None

