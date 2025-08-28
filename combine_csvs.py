def combine_csv_files_efficiently(output_file, input_files):
    """Efficiently concatenates multiple CSV files."""
    print(f"--- Combining CSV files into '{output_file}' ---")
    
    with open(output_file, 'w') as outfile:
        first_file = input_files[0]
        print(f"  - Reading {first_file} (with header)...")
        with open(first_file, 'r') as infile:
            header = infile.readline()
            outfile.write(header)
            for line in infile:
                outfile.write(line)

        for f in input_files[1:]:
            print(f"  - Reading {f} (skipping header)...")
            with open(f, 'r') as infile:
                infile.readline()
                for line in infile:
                    outfile.write(line)
    print("--- Combination complete. ---")

if __name__ == "__main__":
    files_to_combine = ["locality_data.csv", "scan_data.csv"]
    combine_csv_files_efficiently("training_data.csv", files_to_combine)
