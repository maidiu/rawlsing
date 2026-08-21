# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 9 REAL-ORACLE NEGATIVE TEST CORRECTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted PostgreSQL UTF-8 harness head: `8eee62ec694dd85d640f8420f1db3d5c84e7ec90`
Accepted PostgreSQL UTF-8 harness SHA-256: `6218ee1adbf1fe6f2ccb3c8c67fa53683b6b5681fcab7fd28020cd6ae6340f1e`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted:

- Stage A / A.1 / A.2
- B1/B2 CLI separation
- real B1 neutral checkpoint
- PostgreSQL UTF-8 correction and proof

Two real B2 attempts are NON-ADMISSIBLE carrier evidence:

1. first failed during PostgreSQL ASCII COPY transport;
2. second passed the corrected PostgreSQL UTF-8 transport and then failed in the shared deliberate wrong-oracle negative test because real Q02 is dictionary-shaped while the test attempted list slicing.

Binding newest authority:

`27_SR04_REAL_ORACLE_NEGATIVE_TEST_CORRECTION_GATE.md`

REAL B2 RETRY IS BLOCKED.

## Immediate mission — cheap oracle-negative-test proof only

Modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No other repository file may change.

Correct only the shared deliberate wrong-oracle negative-test mechanics.

Implement one deterministic shape-agnostic oracle corruption helper that:

- supports dict, list, scalar and null JSON-domain values;
- always returns a deliberately altered value;
- never mutates its input;
- deterministically corrupts non-empty dictionaries using stable key ordering;
- deterministically corrupts non-empty lists;
- uses a deterministic sentinel alteration for empty/scalar values.

Replace the invalid expression:

`oracle["Q02_WVS_Q152_DISTRIBUTION"][:-1]`

with the shared helper-produced corruption.

Do not change oracle construction or normalization to accommodate the test.

## Required cheap proof

Run no carrier court and no raw-source work.

Exercise the exact helper used by shared validation against both:

- a synthetic list-shaped Q02 sample;
- a real-like dictionary-shaped Q02 sample.

Required assertions:

- `synthetic_list_corruption_pass = true`
- `real_dict_corruption_pass = true`
- `synthetic_original_unchanged = true`
- `real_original_unchanged = true`
- `synthetic_wrong_oracle_detected = true`
- `real_wrong_oracle_detected = true`
- `no_exception = true`
- `raw_source_decode = false`
- `checkpoint_mutated = false`
- `carrier_court_executed = false`
- `DATABASE_URL_unused = true`

Required token:

`PRE553_SR04_ORACLE_NEGATIVE_TEST_SHAPE_PROOF_PASS`

The proof may read the accepted checkpoint only to hash it before/after if desired; it must not rewrite it.

## Publication

After the proof passes:

1. syntax/static check;
2. verify only `SR04_CARRIER_BAKEOFF.py` changed;
3. commit only that file;
4. commit message: `Fix SR04 real-oracle negative test`;
5. push the control branch;
6. return to HQ:
   - exact starting HEAD;
   - new harness HEAD;
   - harness SHA-256;
   - exact proof command;
   - complete proof receipt;
   - required token;
   - original/corrupted list samples;
   - original/corrupted dict samples;
   - final `git status -sb`;
   - pushed branch HEAD;
7. STOP.

## Forbidden

Do not:

- run B1;
- run B2;
- pass `--source-root`;
- decode WVS7/LiTS I;
- mutate `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`;
- reopen PostgreSQL UTF-8 transport;
- change Q00-Q15, oracle construction, normalization, replay, timing, indexes, budgets, candidate set, or selection law;
- use or inspect `DATABASE_URL`;
- touch live Rawlsing PostgreSQL;
- commit execution outputs.

Fail closed on ambiguity.
