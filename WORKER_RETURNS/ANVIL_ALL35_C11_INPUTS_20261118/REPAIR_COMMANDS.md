# Proof-harness repair — exact replay commands

Frozen input: `d8758a1b1e776406aac551ccc1b4822ed03639d3`
Q2 interfaces: `aee95429609c372564e996c2d3d3eb30e9253cbf`
All commands run from a checkout root containing `rawlsing_next/`.

## 1. Positive fresh-root replay

Use a new empty output root. The script refuses the canonical return as a root
and refuses any non-empty root, so frozen proofs are not overwritten.

```bash
ROOT=WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/tmp/fresh_repair
rm -rf "$ROOT"
mkdir -p "$ROOT"

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/run.py "$ROOT"
```

Expected final line:

```json
{"TESTONLY_BUNDLE_PASS": true, "root": ".../tmp/fresh_repair"}
```

The run emits and reloads the five typed fixture inputs, performs one actual
`SourceSavedBodySink` build, cold-reopens all 13 families in a fresh process,
and writes:

- `$ROOT/proof/build.json`
- `$ROOT/proof/reopen.json`
- `$ROOT/proof/refusal.json` — census mismatch before source access
- `$ROOT/proof/reopen_refusal_revoked.json`
- `$ROOT/proof/reopen_refusal_wrong_root.json`
- `$ROOT/proof/digest_refusal.json`

## 2. Individual negatives

The positive command already runs all negatives. To run them separately:

```bash
ROOT=WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/tmp/fresh_repair

ANVIL_TESTONLY_ROOT="$ROOT" ANVIL_REOPEN_MODE=revoked \
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/reopen_bundle.py

ANVIL_TESTONLY_ROOT="$ROOT" ANVIL_REOPEN_MODE=wrong_root \
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/reopen_bundle.py

ANVIL_TESTONLY_ROOT="$ROOT" \
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/check_refusal.py

ANVIL_TESTONLY_ROOT="$ROOT" \
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/check_digest.py
```

## 3. Reproduce the old unconditional-authorization defect

The frozen script at `d8758a1b` ignored revocation because it passed
`current_authorizer=lambda _roots: True`:

```bash
git show d8758a1b1e776406aac551ccc1b4822ed03639d3:WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/reopen_bundle.py > /tmp/old_reopen.py
# Run from an equivalent return tree so HERE resolves to the frozen build proof.
```

The recorded reproduction is `evidence/reproduce_old_defect.json`: the old
script exited 0 and printed `reopen: PASS` even with `ANVIL_REOPEN_MODE=revoked`.
The repaired script refuses with `DirectEstateError`.

## 4. Tests

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  --basetemp=WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/tmp/tests_repair \
  WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/tests
```

Expected: `6 passed`.

## 5. Another-checkout replay

The same script was copied to a separate checkout-shaped directory with only
`rawlsing_next` linked, and run with a separate output root:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  <other-checkout>/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/testonly_bundle/run.py \
  <fresh-output-root>
```

Evidence: `evidence/other_checkout_replay.out` (`TESTONLY_BUNDLE_PASS`).

## Boundary

- Sourcefree 5-row fixture only.
- No original source read, hash, decode, or permission issuance.
- No product files.
- No all-35 row removal or admission.
- SRC17 scope correction preserved.
- Canonical frozen `testonly_bundle/proof/` is not rewritten by the replay.
