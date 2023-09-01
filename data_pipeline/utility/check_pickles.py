import os
import pickle
import numpy as np

# Directory containing the pickles
directory_path = "pickles_train_latest/"

# List all pickle files in the directory
pickle_files = sorted([file for file in os.listdir(directory_path) if file.endswith(".pkl")])

# Loop through each pickle file
for file in pickle_files:
    with open(os.path.join(directory_path, file), 'rb') as f:
        # Load pickle contents
        data = pickle.load(f)
        
        # Ensure the data is a tuple of length 5
        if isinstance(data, tuple) and len(data) == 5:
            std, mean, min_val, max_val, name = data
            print(f"File: {file}")
            print(f"Name: {name}")
            print(f"Std: {std}")
            print(f"Mean: {mean}")
            print(f"Min: {min_val}")
            print(f"Max: {max_val}")
            print('-'*50)
        else:
            print(f"Unexpected data format in {file}")

