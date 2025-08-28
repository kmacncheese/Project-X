from cache import Cache
from policies import LRU_Policy, FIFO_Policy, AI_Policy
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run a cache simulation.")
    parser.add_argument('--policy', type=str, required=True, choices=['lru', 'fifo', 'ai'])
    parser.add_argument('--trace', type=str, required=True)
    args = parser.parse_args()

    if args.policy == 'lru':
        policy = LRU_Policy()
    elif args.policy == 'fifo':
        policy = FIFO_Policy()
    elif args.policy == 'ai':
        policy = AI_Policy()

    cache = Cache(size=1024, policy=policy)
    hits, misses = 0, 0

    with open(args.trace, 'r') as f:
        for line in f:
            address = line.split()[0]
            if cache.access(address):
                hits += 1
            else:
                misses += 1

    total = hits + misses
    hit_rate = (hits / total) * 100 if total > 0 else 0
    print("--- Simulation Complete ---")
    print(f"Trace: {args.trace}")
    print(f"Policy: {args.policy.upper()}")
    print(f"Hits: {hits}, Misses: {misses}, Total: {total}")
    print(f"Hit Rate: {hit_rate:.2f}%")

if __name__ == "__main__":
    main()