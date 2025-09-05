import collections
import csv
import bisect
import argparse

def generate_training_data(trace_file, output_csv, cache_size):
    # Simulates a cache with an oracle to generate labeled training data, including the 'stride' feature.
    print(f"--- Generating data for: {trace_file} ---")
    
    with open(trace_file, 'r') as f:
        trace = [line.split()[0] for line in f]
    print(f"Trace contains {len(trace)} accesses.")

    positions = collections.defaultdict(list)
    for i, address in enumerate(trace):
        positions[address].append(i)

    cache = set()
    recency = collections.defaultdict(int)
    frequency = collections.defaultdict(int)
    previous_address = 0
    training_examples = []

    for i, address_str in enumerate(trace):
        address_int = int(address_str, 16)
        stride = address_int - previous_address

        for page in list(recency.keys()):
            recency[page] += 1

        recency[address_str] = 0
        frequency[address_str] += 1

        if address_str not in cache:
            if len(cache) >= cache_size:
                future_uses = {}
                for page_in_cache in cache:
                    pos_list = positions[page_in_cache]
                    insertion_point = bisect.bisect_right(pos_list, i)
                    
                    if insertion_point < len(pos_list):
                        future_uses[page_in_cache] = pos_list[insertion_point]
                    else:
                        future_uses[page_in_cache] = float('inf')

                oracle_victim = max(future_uses, key=future_uses.get)

                for page_to_consider in cache:
                    features = {
                        'recency': recency[page_to_consider],
                        'frequency': frequency[page_to_consider],
                        'stride': stride,
                        'should_evict': 1 if page_to_consider == oracle_victim else 0
                    }
                    training_examples.append(features)
                cache.remove(oracle_victim)
            cache.add(address_str)
        previous_address = address_int
            
    print(f"Writing data to {output_csv}...")
    fieldnames = ['recency', 'frequency', 'stride', 'should_evict']
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(training_examples)
    
    print(f"--- Data generation for {trace_file} complete. ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate training data.")
    parser.add_argument('--trace_file', type=str, required=True)
    parser.add_argument('--output_csv', type=str, required=True)
    parser.add_argument('--cache_size', type=int, default=1024)
    args = parser.parse_args()
    generate_training_data(args.trace_file, args.output_csv, args.cache_size)
