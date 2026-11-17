# R4 RAW COMMANDS AND EXITS

All R4 paths are under `WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R4_RECHECK/`.

## Target/archive

```text
git -C .../INTEGRATION rev-parse HEAD
05e81747fb2e5cca042c0d968ba1ae203182556e
shasum -a 256 .../REPAIRED_PACKAGE.zip
701207ec43eb1975e66f6dc324da7a9c786a84800d0ae16e9e2e4526d62daad9  (1,858,438 bytes)
```

Target ZIP hash matches `git show 05e81747:.../REPAIRED_PACKAGE.zip`; `MANIFEST.json`, `R4_DEFECT_CLOSURE.md`, `RETURN.md`, `HOLDS.md`, `SOURCE_AUTHENTICATION.json` match Git. Manifest rehash: **1142/1142**, 0 missing/bad. ZIP copied to `INPUT/REPAIRED_PACKAGE_R4.zip`, extracted fresh to `COLD/FRESH_<stamp>`.

## Literal cold commands (from `.../ANVIL_R7/tools`)

```text
python3 r7_inventory.py verify --source-root ../EVIDENCE/SOURCE_118 --repo /Users/matthewsmith/s2b-work/rawlsing --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip --inventory ../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json
exit 0  PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY; 118; zero errors.

python3 -m unittest test_r7_integrated -q
exit 0  Ran 29 tests ... OK.

python3 test_integrated_strict.py
exit 0  Ran 11 tests ... OK.

python3 r7_integrated.py FRAME ... ; DECISION ... ; C_INTEGRATED ...
exit 0 all: PASS local statuses; C_HOLD_EXACT.

python3 r7_build.py verify ../EVIDENCE/DECISION.json ... --out ../BUILT
exit 0  PASS_SIX_PROJECTIONS_BYTE_IDENTICAL.
```

Logs: `LOGS/literal_inventory.log`, `literal_29.log`, `literal_11.log`, `literal_{FRAME,DECISION,C_INTEGRATED}.log`, `literal_build.log`.

## State/claim witness

```text
python3 WITNESS/r4_state_witness.py
```

exit 0. Result `WITNESS/W_STATE_CLAIM/r4_state_claim.json`:
- baseline FRAME/DECISION/C PASS;
- P4R-R01 hold→present: RED;
- REQ-FIELD-FORGE future→present: RED;
- T4 source-static→actual without witness: C RED;
- T4 with fake witness: C RED;
- analog P4R-R02, REQ-SEAM-WORLD-ACTOR, T6: RED;
- coherent recomputed flags/hashes/evidence grade: RED;
- exact baseline restore: PASS;
- changed proposal: PASS; changed source fate: RED (versioned review required).

## Custody

R1/R2/R3 files untouched; R4 uses only R4 output paths; target/candidate read-only. No copied witness hardcodes an old review root.
