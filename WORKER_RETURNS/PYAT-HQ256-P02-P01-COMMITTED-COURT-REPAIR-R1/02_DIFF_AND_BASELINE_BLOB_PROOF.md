# HQ256 P02 — exact diff and baseline-blob proof

## 1. The complete change — ONE test function in ONE file

`rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py`

No other test function was touched. No production file was touched. No refusal precedence or set
semantics changed.

Removed:

```python
def test_adopted_binder_baseline_was_the_unmodified_owner():
    """Record the baseline blob this candidate was written against."""
    import pathlib
    import subprocess

    path = pathlib.Path("rawlsing_next/pre553_service_f8_source_scope_binding.py")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD:" + str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    assert head == BINDER_BASELINE_BLOB, (
        "the candidate must be written against the recorded adopted baseline")
    assert B.__file__.endswith("pre553_service_f8_source_scope_binding.py")
```

Added:

```python
def test_adopted_binder_baseline_is_pinned_to_a_fixed_commit_not_head():
    """HQ256 P02 REPAIR. The provenance guard is HEAD-independent."""
    import hashlib
    import pathlib
    import subprocess

    p01_base_commit = "428be7595fce3ecf6ae3cb37852bee884d9ce2e1"
    p01_candidate_commit = "23438ab52f16abda5960a075dfca3f4d3396eab5"
    baseline_blob = "4ba00b8ecf73f70ad0f6481e255fd0117744418a"
    candidate_blob = "848d2d0eedb04b792747e9d6aaa49bb39d108a2c"
    candidate_sha256 = (
        "5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b")

    # layer A -- git-free, always executed
    assert BINDER_BASELINE_BLOB == baseline_blob
    assert baseline_blob != candidate_blob

    path = pathlib.Path("rawlsing_next/pre553_service_f8_source_scope_binding.py")
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == candidate_sha256
    assert raw.decode("utf-8").count("BINDING_PERMISSION_IDENTITY_MISMATCH") == 1
    assert B.__file__.endswith("pre553_service_f8_source_scope_binding.py")

    # layer B -- git at FIXED commits; skipped, never failed, without git
    def _blob(commit: str):
        result = subprocess.run(
            ["git", "rev-parse", commit + ":" + str(path)],
            capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return result.stdout.strip()

    baseline_at_base = _blob(p01_base_commit)
    candidate_at_commit = _blob(p01_candidate_commit)
    if baseline_at_base is None or candidate_at_commit is None:
        pytest.skip("no git object store available: fixed-commit identity layer not "
                    "executable here (terrain limitation, not a defect)")
    assert baseline_at_base == baseline_blob
    assert candidate_at_commit == candidate_blob
    assert _blob("HEAD") == candidate_blob
```

## 2. Baseline-blob proof — measured, not asserted

Every identity below was read from the object store rather than taken on trust.

| identity | measured value | source |
|---|---|---|
| binder blob at P01 base `428be7595…` | `4ba00b8ecf73f70ad0f6481e255fd0117744418a` | `git rev-parse` |
| binder blob at P01 candidate `23438ab52…` | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` | `git rev-parse` |
| `git hash-object` of the working file | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` | HEAD-independent |
| sha256 of the working file | `5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b` | `hashlib`, git-free |
| sha256 of the baseline file | `0a5d3020572f1d72dd9b4a200d2a98176587cf3282714022ccfe910519900c75` | `hashlib`, git-free |
| refusal code occurrences in baseline blob | **0** | counted from `git show` |
| refusal code occurrences in candidate blob | **1** | counted from `git show` |

Both fixed commits resolve as commits in this object store, so layer B is genuinely **executable**
here rather than being skipped.

I independently reproduced R01's vocabulary claim: the refusal code is absent from the baseline
blob and appears exactly once in the candidate.

## 3. Why the old assertion could never certify the candidate

The old guard asserted `HEAD == baseline`. Since committing the candidate *is* precisely what
moves `HEAD` off the baseline, the assertion and the artefact it guarded were mutually exclusive:

| state of the production binder | `HEAD` binder blob | old guard | new guard |
|---|---|---|---|
| candidate **uncommitted** | baseline | **PASS** (accidentally) | **FAIL** (candidate absent from disk) |
| candidate **committed** | candidate | **FAIL** (always) | **PASS** ✅ |

The original "16 passed" was therefore only reachable in a state that is **not** the deliverable.
The repaired court passes only in the state that actually matters, and fails when the reviewed
candidate is absent from disk — which is exactly what makes it a real discriminator rather than a
permanently-broken assertion.

## 4. Production binder byte-identity across the whole lane

After every revert/restore cycle used for the negative controls:

```
git diff --stat -- rawlsing_next/pre553_service_f8_source_scope_binding.py   ->   (empty)
sha256                                                                     5221d8c2…  (unchanged)
bytes                                                                             56186  (unchanged)
```

No production line required adjustment, so the commission's stop-and-request-a-fresh-commission
condition never arose.

## 5. Changed terrain — exactly one source path

| path | change | authorized |
|---|---|---|
| `rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py` | 1 test function repaired | "Allowed edit exactly" |
| `WORKER_RETURNS/PYAT-HQ256-P02-P01-COMMITTED-COURT-REPAIR-R1/` | 4 return files | "own return" |

No production module, no other test, no control / HQ / semantic / warrant path, no issuer or native
path. No permission issuance, no self-adoption.