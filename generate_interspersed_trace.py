# generate_interspersed_trace.py
import random

def generate_interspersed_trace(filename, num_lines):
    """
    Generates a trace where high-locality accesses are
    interspersed with a scan.
    """
    print(f"Generating interspersed scan trace file: {filename}")
    
    # A small set of valuable pages
    hot_addresses = [f"0x{i*4096:08x}" for i in range(100)]
    scan_base_address = 0x80000000
    scan_counter = 0
    
    with open(filename, 'w') as f:
        for i in range(num_lines):
            # 4 out of 5 accesses are to hot pages
            if i % 5 != 4:
                address = random.choice(hot_addresses)
                f.write(f"{address} R\n")
            # 1 out of 5 accesses is a unique scan page
            else:
                address = f"0x{scan_base_address + scan_counter*64:08x}"
                f.write(f"{address} R\n")
                scan_counter += 1
                
    print("Done.")

if __name__ == "__main__":
    generate_interspersed_trace("traces/interspersed_scan_trace.txt", 100000)