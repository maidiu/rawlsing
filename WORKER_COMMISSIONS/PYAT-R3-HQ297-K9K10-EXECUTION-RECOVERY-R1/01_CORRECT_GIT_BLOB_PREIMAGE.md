# K9E precise Git blob preimage correction

The prose formula in 00_COMMISSION.md displays `\\0` ambiguously. **Use an actual NUL byte (`0x00`) in the Git blob hash preimage**, not the two ASCII characters backslash and zero. The correct Python code is:

```python
import hashlib

def git_blob_sha1(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + bytes([0]) + content).hexdigest()
```

Compute source `content` from exact fetched bytes, not transformed Markdown or modified whitespace; verify PE module blob `58484f4c3d9aae148d4116dcf00420c432aefcbd` and frozen SC0 K9/K10 Git blobs before execution. Do not treat a failed digest after normalized newlines as source corruption until inspecting the content transport. This supplement is part of the new sealed startup and only clarifies provenance math; all scope/permission constraints in 00 remain.
