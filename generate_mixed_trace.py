# generate_mixed_trace.py
import random

def generate_mixed_trace(filename, locality_lines, scan_lines):
    """
    Generates a trace that first establishes locality, then introduces a scan.
    """
    print(f"Generating mixed-workload trace file: {filename}")
    
    hot_addresses = [f"0x{i*4096:08x}" for i in range(500)] # Valuable pages
    
    with open(filename, 'w') as f:
        # Phase 1: Establish valuable pages in the cache
        print("Phase 1: Establishing locality...")
        for _ in range(locality_lines):
            address = random.choice(hot_addresses)
            f.write(f"{address} R\n")
            
        # Phase 2: Introduce a long, cache-destroying scan
        print("Phase 2: Introducing scan...")
        scan_base_address = 0x80000000
        for i in range(scan_lines):
            address = f"0x{scan_base_address + i*64:08x}"
            f.write(f"{address} R\n")
            
        # Phase 3: Revisit the valuable pages
        print("Phase 3: Revisiting valuable pages...")
        for _ in range(locality_lines):
            address = random.choice(hot_addresses)
            f.write(f"{address} R\n")

    print("Done.")

if __name__ == "__main__":
    # 20k locality accesses, then a 60k scan, then 20k more locality accesses
    generate_mixed_trace("traces/mixed_final_trace.txt", 20000, 60000)