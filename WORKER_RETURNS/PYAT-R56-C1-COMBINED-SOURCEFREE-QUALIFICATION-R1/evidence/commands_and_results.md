# R56-C1 — exact commands, exits and observed results

All runs in `/Users/matthewsmith/Desktop/Rawlsing/R56-C1-combined-sourcefree-qualification-wt`.
Host macOS 13.2.1; Python 3.11.3; pytest 9.0.2; pyreadstat 1.3.2; pandas 2.3.1.

## Assembly

```
git cat-file blob e31ed756... > CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py
git cat-file blob a6299c1a... > rawlsing_next/pre553_source_native_preimage_adapter.py
git hash-object <both> -> e31ed756... / a6299c1a...       (pins match)
git hash-object rawlsing_next/pre553_physical_decoder.py -> 8732e34d...  (unchanged)
git commit -> composite a2aeb53b0a1e6abb93d4bb3d173007002fd7cf44
```

Accepted tests copied from `d02ef322` (R00, 7 blobs) and `e1f0aeb6` (R02,
test+proof blobs); all `git hash-object` results match the review refs. R04
byte test preserved at startup blob `76a2a17a...`.

## Combined suites (one run on the combined tree)

```
python3 -m pytest tests/universal_execution_oracle \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py -q -rs
169 passed, 1 skipped in 68.89s      exit 0
SKIPPED rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py:268 installed
pyreadstat writer/readback does not expose missing_user_values in metadata
```

## C1 focused test module

```
python3 -m pytest tests/universal_execution_oracle/test_c1_combined_sourcefree.py -q
7 passed                              exit 0
```

## Proof integrity

```
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint <C1 test>
AST_LINT_PASS                         exit 0
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness <C1 proof> --root .
2/2 baseline PASS, 2/2 TARGET_ASSERTION_FAILED, adapter restored a6299c1a...
exit 0
fresh positive nodes after witness: 2 passed
```

## Combined path / custody receipt (`probe_combined_path.json`)

- SAV 4x2: source sha `73501d2d...`, SUPPORTED, denominator 4, numerator 4,
  fact ref `a695125c...`, 8 exact tuples, 4 cells; DTA: `3439a489...`,
  SUPPORTED, denominator 4, fact ref `2c1aa47c...`.
- Original-path replacement: same fact; private-path replacement: same fact,
  foreign survives close; write/pwrite/ftruncate/mmap/reopen denials:
  errno 9/9/22/13/13; digest and fact unchanged.
- Normalized source-key collision: `DUPLICATE_NORMALIZED_SOURCE_KEY`.
- Value fault changes the same query; exact restore same fact.

## R00 gate receipt (`probe_r00_gate.json`)

- Policy `6d95a78b`, CANONICAL_V1, verified true; blobs `CONTRACT 01ccb464`,
  `policy 5f5d0253`, `synthetic_universes 66fdf81f`,
  `decision_cases 5608e9c3`, `freeze dfc1c375`.
- POLICY_ONLY complete -> `ALLOW_LOCAL_POLICY_CONSISTENT` (ceiling local-only);
  missing and altered frontier -> `REFUSE_FRONTIER`; EXECUTED_NATIVE without
  R09 -> `HOLD_TRUSTED_NATIVE`; GENERIC_SOURCEFREE -> `HOLD_GENERIC_R09`;
  supported status without evidence -> HOLD/refuse; K_mutation ->
  `REFUSE_IDENTITY` (policy marker, NOT native association); policy
  substitution -> `REFUSE_FRONTIER`; restore -> ALLOW.
- No verified-evidence handle; no native-positive gate verdict.

## Final SHA/readback

Recorded in `evidence/final_remote_readback.json` after push: remote branch SHA,
ancestry, changed-file allowlist, and final test-tree commit SHA.
