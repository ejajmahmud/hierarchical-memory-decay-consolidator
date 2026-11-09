"""CLI for hierarchical-memory-decay-consolidator."""
import sys
import argparse
from .consolidator import HierarchicalMemory


def main():
    parser = argparse.ArgumentParser(description="Hierarchical Memory Decay Consolidator CLI")
    parser.add_argument("--demo", action="store_true", help="Run hierarchical memory consolidation demo")
    args = parser.parse_args()

    if args.demo:
        mem = HierarchicalMemory(working_half_life=10.0, episodic_half_life=50.0)
        mem.store("user_temp_var", "12345", salience=0.5)
        mem.store("user_preference", "Dark theme", salience=1.0)

        # Access preference repeatedly to consolidate into Semantic
        for _ in range(6):
            mem.retrieve("user_preference")

        print("Before Decay Cycle:")
        for k, v in mem.entries.items():
            print(f"  [{v.tier.value}] {k} -> Salience: {v.salience:.2f} (Access: {v.access_count})")

        print("
Simulating 30 seconds of decay...")
        mem.run_decay_cycle(30.0)

        print("After Decay Cycle:")
        for k, v in mem.entries.items():
            print(f"  [{v.tier.value}] {k} -> Salience: {v.salience:.2f}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
