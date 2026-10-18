"""Deterministically recover precommitted Phase-A JSON input matrix; never rewrite it."""
import gzip, hashlib, pathlib, sys
R=pathlib.Path(__file__).resolve().parent
raw=gzip.decompress((R/'01_FROZEN_HOSTILE_MATRIX.json.gz').read_bytes())
expected='2d16c3fd3d8792e990cfc925a92092d1736d60b6b82638e303c80603a331dd27'
assert hashlib.sha256(raw).hexdigest()==expected,'FROZEN_MATRIX_CONTENT_HASH_MISMATCH'
target=R/'01_FROZEN_HOSTILE_MATRIX.json'
if target.exists():
    assert target.read_bytes()==raw,'REFUSE_EXISTING_DIFFERENT_FROZEN_MATRIX'
else:
    target.write_bytes(raw)
print('FROZEN_MATRIX_SHA256',expected)
