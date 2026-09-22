# PREMAIN FIABC LiTS ASTRA Substantive Parity R1 — Return

## Status

**IMPLEMENTATION COMPLETE / STATIC CONTRACT AUDIT PASS / SOURCE-FREE TEST SUITE AUTHORED / TEST EXECUTION NOT AVAILABLE IN THIS BROWSER+GITHUB-ONLY LANE WITHOUT TRIGGERING GITHUB ACTIONS.**

The success terminal is therefore intentionally **not** self-issued here. The implementation makes substantive parity a fail-closed precondition of LiTS oracle construction, but this worker does not claim an unexecuted suite is green.

## Exact base

`4513eae0ec2c55c3252871c77cd52fc3dd0f07cd`

Branch:

`agent/rabochii-premain-fiabc-lits-astra-substantive-parity-r1`

The exact final branch head is reported by the worker terminal after the return commit, because a Git commit cannot contain its own not-yet-created SHA.

## Immutable ASTRA authority consumed

Accepted historical commit:

`e631de162c582423639b7067a4f36b29f8aa4d89`

Exact inputs and pinned Git blob identities:

- `WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json` — blob `26fa18d10d242f3db212f6ee3e6f28abee3327ac`
- `WORKER_RETURNS/ASTRA-D04-R2/02_77_ROLE_EXECUTION_RECEIPT.json` — blob `211e19bb17cd8e3c63418b686ac20508072cb7d7`
- `WORKER_RETURNS/ASTRA-D04-R2/03_SOURCE_AND_REPLAY_RECEIPT.json` — blob `b2c70e992955853b540e498214c296ccc0e25b83`

Historical source identity bound by the parity receipt:

- LiTS-I SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows `29002`
- variables `1198`

## Repair

Added `rawlsing_next/fiabc_lits_astra_substantive_parity.py`.

The new gate:

1. deterministically normalizes immutable ASTRA-D04-R2 empirical evidence into an ASTRA-shaped truth summary;
2. deterministically normalizes the current candidate-neutral PRE553 I05 result into the same restricted summary;
3. exact-compares frontier, D03 roots, all 77 role states, per-role risk-set ownership, P0, P1, all 18 P2 witnesses, P3 exact false-reversal semantics, all 25 located P4 cell supports, and final 49+1 envelope;
4. persists a deterministic auditable parity receipt;
5. only then permits `build_lits_i_oracle()`.

Parity failure raises before oracle construction.

## Substance represented

**P0–P4 accepted empirical substance represented: YES.**

- P0: all five exact denominators/supports and ASTRA-recorded candidate hashes.
- P1: exact candidate identity, joint witness, both marginals, denominators, supports, and explicit non-product relationship.
- P2: all 18 ASTRA-recorded candidate hashes and their exact first-difference witnesses.
- P3: exact candidate identity, eight exact rates, pooled sign, three stratum signs, and the accepted mechanism `VALIDATION_FALSE__NO_CONDITIONAL_REVERSAL`; all eight current role facts must be positive-denominator `SUPPORTED`, so zero-support/unresolved emptiness cannot masquerade as the accepted valid-empty.
- P4: all 25 supports keyed by exact 5×5 cell location. Multiset-preserving cell permutations fail.

## D03 / role execution

Accepted roots are exact:

- R2: count `24897`, root `f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3`
- R7: count `28325`, root `0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844`
- R27: count `24630`, root `f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29`

Current execution facts must expose the exact corresponding risk-member cardinality for every logical role. The current D03 authority itself is root-pinned, so the three distinct counts identify the required R2/R7/R27 role assignment without deriving membership from current values.

All 77 roles must normalize to `SUPPORTED`; terminal candidate counts alone are not sufficient.

## Freeze boundary

**Parity executes before oracle freeze: YES.**

Order in `produce_lits_local_oracle()`:

current neutral execution → current ASTRA-shaped summary → immutable ASTRA inputs → accepted ASTRA-shaped summary → exact substantive parity → persisted receipt → `build_lits_i_oracle()`.

No oracle build call occurs on parity failure.

## Hash-domain law

**Incompatible historical/current whole-object hashes compared for equality: NO.**

Historical ASTRA whole-product/replay identities remain immutable provenance checks inside the historical schema. Current execution/replay identities remain current-schema identities. The parity receipt explicitly records:

- `historical_current_whole_object_hash_equality_required = false`
- `whole_object_hashes_compared_across_schema_domains = false`

Only the normalized empirical substance crosses the schema boundary.

## Hostile tests

Source-free hostile suite added:

`rawlsing_next/tests/test_fiabc_lits_astra_substantive_parity.py`

It contains **27 pytest cases after parameter expansion**, covering every one of the 22 commissioned hostile requirements plus direct current-normalizer fixtures and noninterference checks.

Execution status in this worker lane: **NOT RUN**. No GitHub Actions workflow was triggered.

## WVS7 noninterference

**WVS7 oracle path changed: NO.**

No WVS7 producer/oracle implementation was edited. A source-free test asserts the WVS standardization function has no LiTS/ASTRA parity dependency.

## Prohibited activity audit

- source files opened = **false**
- raw LiTS/WVS source materialized = **false**
- source-backed I05 run = **false**
- Candidate A/B/C run = **false**
- measured P2X run = **false**
- P3 run = **false**
- architecture selection performed = **false**
- governed execution branch mutated = **false**
- user Mac used = **false**
- GitHub Actions triggered = **false**
