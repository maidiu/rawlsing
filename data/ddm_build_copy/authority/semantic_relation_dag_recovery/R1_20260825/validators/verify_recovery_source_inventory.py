#!/usr/bin/env python3
from pathlib import Path
import hashlib, re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"provenance"/"RECOVERED_FROM_LIBRARY_DATE_SIZE_SHA256_TREE.tsv"
side=ROOT/"provenance"/"RECOVERED_FROM_LIBRARY_DATE_SIZE_SHA256_TREE.tsv.sha256"
expected=side.read_text().strip().split()[0]
actual=hashlib.sha256(p.read_bytes()).hexdigest()
assert expected==actual, f"source inventory SHA mismatch: {actual} != {expected}"
print(f"PASS source_inventory_sha256={actual}")
