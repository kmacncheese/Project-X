import random

def generate_fake_trace(filename, num_lines):
    #Generates a high-locality trace file.
    print(f"Generating high-locality trace file: {filename}")
    hot_addresses = [f"0x{i*4096:08x}" for i in range(10)]
    
    with open(filename, 'w') as f:
        for i in range(num_lines):
            if random.random() < 0.8:
                address = random.choice(hot_addresses)
            else:
                address = f"0x{random.randint(1000, 9999)*4096:08x}"
            f.write(f"{address} R\n")
    print("Done.")

if __name__ == "__main__":
    generate_fake_trace("traces/fake_locality_trace.txt", 100000)