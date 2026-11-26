import kagglehub
import os
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("meruvulikith/190k-spam-ham-email-dataset-for-classification")

print("Path to dataset files:", path)

# List files in the path
files = os.listdir(path)
print("Files in dataset:", files)

# Try to read the first CSV file found
for file in files:
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(path, file), nrows=100) # Read only 100 rows for inspection
        print(f"\nColumns in {file}:", df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head())
        print("\nUnique values in first column (likely label):", df.iloc[:, 0].unique())
        break
