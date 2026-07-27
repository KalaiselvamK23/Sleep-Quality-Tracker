import numpy as np
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "Sleep_Efficiency.csv"

df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "equilibriumm/sleep-efficiency",
    file_path
    # Documentation for more information:
    # https://github.com/Kaggle/kaggle/blob/main/README.md#kaggledatasetadapterpandas
)

print("First 5 records:")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nData types:")
print(df.dtypes)