import os
import sys

# Ensure workspace root is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from jocky.cli import main

if __name__ == "__main__":
    # If no arguments provided, default to running the investigation case
    if len(sys.argv) == 1:
        print("\n[JOCKY] No command specified. Defaulting to: run investigation/case.jky\n")
        sys.argv.extend(["run", "investigation/case.jky"])
    main()
