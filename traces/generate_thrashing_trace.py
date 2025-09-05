import random

def generate_thrashing_trace(filename, num_lines):
    # Generates a trace that first causes cache thrashing with a large locality set, then introduces a scan to defeat LRU.
    print(f"Generating thrashing + scan trace file: {filename}")
    
    # CRITICAL: The number of hot addresses is > cache size (1024)
    hot_addresses = [f"0x{i*4096:08x}" for i in range(1100)]
    scan_base_address = 0x80000000
    scan_counter = 0
    
    with open(filename, 'w') as f:
        for i in range(num_lines):
            # 9 out of 10 accesses are to the thrashing hot set
            if i % 10 != 9:
                address = random.choice(hot_addresses)
                f.write(f"{address} R\n")
            # 1 out of 10 accesses is a unique scan page
            else:
                address = f"0x{scan_base_address + scan_counter*64:08x}"
                f.write(f"{address} R\n")
                scan_counter += 1
                
    print("Done.")

if __name__ == "__main__":
    generate_thrashing_trace("traces/thrashing_scan_trace.txt", 100000)