# SR04 — REAL-ORACLE NEGATIVE-TEST CORRECTION GATE

Repository: `maidiu/rawlsing`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted PostgreSQL UTF-8 harness head: `8eee62ec694dd85d640f8420f1db3d5c84e7ec90`
Accepted PostgreSQL UTF-8 harness SHA-256: `6218ee1adbf1fe6f2ccb3c8c67fa53683b6b5681fcab7fd28020cd6ae6340f1e`

## Status

A second real B2 attempt from authorized control HEAD `f8bbdbbb223968418be5d3029c1543dcfa373147` failed closed after the corrected PostgreSQL UTF-8 transport completed.

Exact failure class:

`SHARED_NEGATIVE_ORACLE_TEST_SHAPE_ASSUMPTION__NO_CARRIER_DISPOSITION`

Observed error:

`unhashable type: 'slice'`

The failing shared validation expression is:

`oracle["Q02_WVS_Q152_DISTRIBUTION"][:-1]`

The accepted synthetic oracle represents Q02 as a list-like normalized row collection, while the real checkpoint oracle represents Q02 as a dictionary. Slicing the real dictionary raises before the deliberate wrong-oracle test can be evaluated.

The B1 checkpoint remains accepted and byte-identical. The PostgreSQL UTF-8 correction is not reopened. No carrier selection or candidate disposition is admissible from this failed run.

## Frozen correction

Modify only the deliberate wrong-oracle negative-test mechanics.

Introduce one deterministic, shape-agnostic corruption helper used by the shared validation path. It must return a value unequal to its input without mutating the input and must support the JSON-domain shapes the oracle can contain:

- dictionary;
- list;
- scalar / null as defensive fallback.

For a non-empty dictionary, deterministically remove or alter one key/value using stable key ordering. For a non-empty list, deterministically remove or alter one element. Empty/scalar values must receive a deterministic sentinel alteration.

Then replace the list-only slicing expression with comparison against the helper-produced corrupted Q02 oracle value.

The negative test remains a test of the validator: the observed correct result must differ from the deliberately corrupted oracle.

Do not change:

- Q00-Q15 truth conditions;
- real or synthetic oracle construction;
- result normalization;
- candidate materialization;
- replay digest logic;
- PostgreSQL UTF-8 transport;
- timing/index/budget/selection law;
- checkpoint format or bytes;
- source decoding;
- any carrier-specific semantics.

## Required cheap proof before another B2 retry

Do not run B2 while implementing this correction.

Add a tiny isolated proof mode using the exact corruption helper called by the shared validation path.

It must prove at minimum:

1. synthetic-list-shaped Q02 sample is corrupted without exception;
2. real-dictionary-shaped Q02 sample is corrupted without exception;
3. corrupted list != original list;
4. corrupted dictionary != original dictionary;
5. original list remains unchanged;
6. original dictionary remains unchanged;
7. shared wrong-oracle predicate evaluates true for both shapes;
8. no raw source decode;
9. no checkpoint mutation;
10. no carrier court execution;
11. `DATABASE_URL` unused.

Required token:

`PRE553_SR04_ORACLE_NEGATIVE_TEST_SHAPE_PROOF_PASS`

## Publication law

Codex may modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

After the cheap proof passes:

1. syntax/static check;
2. verify only the harness changed;
3. commit only the harness;
4. commit message: `Fix SR04 real-oracle negative test`;
5. push the control branch;
6. return exact starting HEAD, new harness HEAD, harness SHA-256, proof command, complete proof receipt/token, final git status, pushed branch HEAD;
7. STOP.

A further real B2 retry requires separate HQ authorization after static review of the committed correction.

## Forbidden

Do not:

- rerun B1;
- run B2 during the cheap proof;
- decode WVS7 or LiTS I;
- mutate or regenerate the accepted B1 checkpoint;
- change the oracle itself to fit the negative test;
- convert real dictionary oracle values to synthetic list form globally;
- use `DATABASE_URL` or live Rawlsing PostgreSQL;
- change carrier/query/replay/performance/selection semantics;
- treat either failed B2 attempt as carrier evidence.
