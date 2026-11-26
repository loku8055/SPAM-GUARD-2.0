import kagglehub
import os
import pandas as pd

path = kagglehub.dataset_download("ashfakyeafi/spam-email-classification")
csv_path = os.path.join(path, "email.csv")
df = pd.read_csv(csv_path)

print("Unique values in Category:", df['Category'].unique())
print("NaN count in Category:", df['Category'].isna().sum())
print("NaN count in Message:", df['Message'].isna().sum())
