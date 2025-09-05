def generate_scan_trace(filename, num_lines):
    # Generates a scan-heavy, 'LRU-killer' trace file.
    print(f"Generating scan-heavy trace file: {filename}")
    base_address = 0x80000000 
    
    with open(filename, 'w') as f:
        for i in range(num_lines):
            address = f"0x{base_address + i*64:08x}"
            f.write(f"{address} R\n")
    print("Done.")

if __name__ == "__main__":
    generate_scan_trace("traces/lru_killer_trace.txt", 100000)