# R3 RAW COMMANDS AND EXITS

All R3 paths are under `WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R3_RECHECK/`. R1/R2 untouched.

## Target/archive

```text
git -C .../INTEGRATION rev-parse HEAD
9fe1fd3842ee1c1c76da0188150467e4799079cc
shasum -a 256 .../REPAIRED_PACKAGE.zip
a4f881e751286f9a881bd7cd433b03a0bfbcf937affc4ac612f72b36357d9ef3  (1,858,176 bytes)
```

Target ZIP hash equals `git show 9fe1fd3:.../REPAIRED_PACKAGE.zip`; target `MANIFEST.json`, `R3_DEFECT_CLOSURE.md`, `RETURN.md`, `HOLDS.md`, `SOURCE_AUTHENTICATION.json` match `git show 9fe1fd3:path`. Manifest rehash: **1012/1012**, 0 missing/bad. New ZIP copied to `INPUT/REPAIRED_PACKAGE_R3.zip`, extracted to `COLD/FRESH_<stamp>` (339 files).

## Literal cold commands (from `.../ANVIL_R7/tools`)

```text
python3 r7_inventory.py verify --source-root ../EVIDENCE/SOURCE_118 --repo /Users/matthewsmith/s2b-work/rawlsing --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip --inventory ../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json
exit 0  PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY; 118; zero errors.

python3 -m unittest test_r7_integrated -q
exit 0  Ran 29 tests ... OK.

python3 test_integrated_strict.py
exit 0  Ran 11 tests ... OK.

python3 r7_integrated.py FRAME ../EVIDENCE/FRAME.json ... ; DECISION ... ; C_INTEGRATED ...
exit 0 for all: PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED; PASS_LOCAL_INTEGRATED_DECISION_PENDING_C; PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED.

python3 r7_build.py verify ../EVIDENCE/DECISION.json ... --out ../BUILT
exit 0  PASS_SIX_PROJECTIONS_BYTE_IDENTICAL.
```

Logs: `LOGS/literal_inventory.log`, `literal_29.log`, `literal_11.log`, `literal_{FRAME,DECISION,C_INTEGRATED}.log`, `literal_build.log`.

## R3 witnesses

```text
python3 WITNESS/r3_witnesses.py
```
exit 0. Results in `WITNESS/r3_results.json`:
- W1a false typed F4 → FRAME/DECISION RED `TYPED_MACHINE_ASSERTION_MISMATCH`.
- W1b pairwise-only prose → FRAME/DECISION RED `NARRATIVE_NOT_REVIEWED_OR_CHANGED`.
- W1c false identity fate with true excerpt → DECISION RED narrative.
- W1d absent witness → FRAME RED typed mismatch.
- W2a original T4/T6/T7 paraphrase → C RED boundary narrative.
- W2b false typed T4 → C RED typed/narrative.
- W2c changed C prose → C RED `PROSE_NARRATIVE_NOT_REVIEWED_OR_CHANGED`.
- W5a F5 hold relabel → DECISION/C RED placeholder/hold/mismatch.
- W5b F5 disconnect + filler, counts 43/58 → DECISION/C RED `TERMINAL_REQUIRED_EDGE_ABSENT`.
- W3 forged external flag/conditional admit → C RED `CONDITIONAL_ADMIT_REQUIRES_TRUSTED_EXTERNAL_CUSTODY_NOT_AVAILABLE`.
- USABILITY changed proposal → DECISION PASS (legitimate proposed; C remains HOLD).
- USABILITY changed source fate → DECISION RED (versioned source/claim review required).

```text
python3 WITNESS/w_state_claim.py
```
exit 0. Results in `WITNESS/W_STATE_CLAIM/w_state_claim.json`:
- P4R-R01 `EXACT_OWNER_HOLD`→`PRESENT_PRESERVED`: DECISION PASS, C PASS.
- REQ-FIELD-FORGE `FUTURE_NONPRECLUDED`→`PRESENT_PRESERVED`: DECISION PASS, C PASS.
- C T4 `SOURCE_STATIC_CONSERVED`→`ACTUAL_PROVED` with self-asserted `actual_first_reader_verified=true`: DECISION PASS, C PASS.

This is the residual R3-1 false-readiness defect.

## Custody

R1/R2 frozen files were not modified. R3 uses only `R3_RECHECK` output paths; no copied witness ROOT/OUT points at an older review. The target/candidate is read-only.
