# inspect_scan_data.py
import pandas as pd

SCAN_DATA_FILE = "scan_data.csv"

print(f"--- Inspecting: {SCAN_DATA_FILE} ---\n")

try:
    df = pd.read_csv(SCAN_DATA_FILE)
    
    print("--- First 10 training examples from the scan trace ---")
    print(df.head(10))
    
    print("\n--- Stride Value Analysis ---")
    # Check the unique values in the stride column
    unique_strides = df['stride'].unique()
    print(f"Unique stride values found: {unique_strides[:5]}...") # Print first 5

except FileNotFoundError:
    print(f"Error: {SCAN_DATA_FILE} not found.")
except Exception as e:
    print(f"An error occurred: {e}")