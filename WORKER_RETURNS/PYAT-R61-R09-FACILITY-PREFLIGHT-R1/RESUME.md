# R61 R09F resume

## State

- Verdict: `FACILITY_GAP`.
- Startup: `3470da602618b5c04b1f28885b5ad1835169e2d5`.
- Branch: `agent/opencode-pyat-r61-r09f-facility-preflight-r1`.
- Write root: `WORKER_RETURNS/PYAT-R61-R09-FACILITY-PREFLIGHT-R1/`.
- Final local commit SHA and direct remote SHA are reported in the final
  response after non-force push. `REMOTE_VERIFICATION.md` records the exact
  verification method.
- This is sourcefree `TEST_ONLY`; no adoption, production, source/science,
  protected-CI, N11/N12 or Sorok authority is created.

## What was actually established

1. The commissioned host is macOS 13.2.1 / Darwin 22.3.0 x86_64, uid 501.
2. Docker, Podman, Colima and Lima are absent from this host. `sandbox-exec`
   is present but is used only by a controller probe, is not wired to runtime
   execution, and does not provide a separate principal or demonstrated
   same-UID process exclusion.
3. Controller scheduling, signed grants, HMAC harness attestation, bounded
   process runner and real closed-loop receipts exist and are reusable. They
   are not a protected native-capture boundary. The real loop receipt itself
   records `isolation: UNPROVEN`.
4. The C11 native-owner callables exist, but R09 executes them in the
   candidate-controlled interpreter and the parent seals a child-authored
   JSON observation. Review `25510c8d...` proves P1/P2 forgery and self-root
   admission; this was not rerun.
5. No broker process, separately pinned owner runtime, declarative
   request/receipt transport, or externally pinned issuer admission exists in
   the observed controller/host.

## Exact next action (finite)

Do not patch the same-interpreter wrapper. Obtain the minimum permission in
`00_RETURN.md` and run the one disposable qualification there: separate
candidate and broker principals, broker-owned pinned C11 owner code, typed
declarative operations, broker-authored issuer-signed receipts, pinned verifier
admission, and the positive/P1/P2/wrong-binding/replay/refusal suite. A
container around the same Python wrapper is not the qualification.

## Verify this return

From the repository root:

```sh
/usr/local/bin/python3 - <<'PY'
import hashlib, json
from pathlib import Path
root = Path("WORKER_RETURNS/PYAT-R61-R09-FACILITY-PREFLIGHT-R1")
m = json.loads((root / "manifest.json").read_text())
for entry in m["files"]:
    data = (root / entry["path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
    assert len(data) == entry["size"], entry["path"]
print("manifest OK", len(m["files"]))
PY
```

Then:

```sh
git ls-remote origin refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1
```

The final response states the local `HEAD` and directly observed remote SHA.
