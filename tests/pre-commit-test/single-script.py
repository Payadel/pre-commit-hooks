#!/usr/bin/env python3

import sys

print(f"Hello from {sys.argv[0]}")
if len(sys.argv) > 1:
    print(f"Other arguments: {sys.argv[1:]}")
sys.exit(1)
