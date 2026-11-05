"""Disable one body-hash assertion temporarily and require the exact regression to fail."""
from pathlib import Path
import subprocess
import sys

source = Path("rawlsing_next/_pre553_c11_execution_view.py")
original = source.read_bytes()
condition = b"\n                            or sha256(scalar.as_buffer()).hexdigest() != selectors[offset].ref.content_hash"
assert original.count(condition) == 1
command = [
    sys.executable, "-m", "pytest",
    "rawlsing_next/tests/test_pre553_c11_execution_view.py::test_cache_hit_delete_and_rehashed_same_key_poison_rebuild",
    "-q", "-o", "addopts=", "-p", "no:cacheprovider",
]
subprocess.run(command, check=True)
try:
    source.write_bytes(original.replace(condition, b"", 1))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout, flush=True)
    assert result.returncode == 1 and "assert path.read_bytes() == original_bytes" in result.stdout
finally:
    source.write_bytes(original)
assert source.read_bytes() == original
subprocess.run(command, check=True)
