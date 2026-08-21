# SR04 — REAL-ORACLE CANONICALIZATION / Q01 / FLOAT-COMPARISON CORRECTION GATE

Status: `REAL_B2_NONADMISSIBLE__ORACLE_COMPARISON_LAYER_DEFECT__CHEAP_PROOF_REQUIRED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Accepted B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

Accepted harness before this correction: `ea0d02ffde10a98872e73ea2b1fed8e453246cfb`

Accepted harness SHA-256 before this correction: `12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

## 1. Third REAL B2 attempt — adjudication

The checkpoint-only retry launched from `7380deb2bef7feaeba5a4f5402f3cde08af839fa` and failed closed with exit code `2`.

Observed diagnostics:

- all six accepted checkpoint file identities passed preflight;
- checkpoint total remained `114705938` bytes;
- PostgreSQL UTF-8 transport/lifecycle completed without the prior encoding defect;
- replay digest comparison was `true` for all four candidates;
- deliberate wrong-oracle negative test was `true`;
- stored-corruption negative test was `true`;
- oracle comparison was `false` for all four candidates;
- no final nine-file package, deterministic ZIP, admissible candidate disposition, timing, disk/RSS result, or provisional selection was produced;
- accepted B1 checkpoint remained byte-identical;
- no B2 process remained.

Disposition:

`THIRD_REAL_B2_ATTEMPT_NONADMISSIBLE__STORED_REPLAY_DIAGNOSTIC_PASS__ORACLE_COMPARISON_PATH_INVALID`

No carrier receives evidence for or against selection from this attempt.

## 2. Root cause — exact

Static inspection proves the shared comparison path is structurally inconsistent between synthetic Stage A and real B1.

### 2.1 Frozen B1 oracle shape

`make_oracle()` serializes the accepted real oracle using mixed JSON shapes:

- grouped queries such as Q00/Q01/Q02/Q03/Q04/Q08/Q09/Q10/Q11/Q12/Q13/Q15 -> dictionaries, with multi-column group keys stringified;
- Q05 -> scalar integer;
- Q06 -> scalar float;
- Q07 -> list of record dictionaries;
- Q14 -> label-to-count dictionary.

The accepted B1 `QUERY_ORACLE.json` byte identity and digest remain frozen. It MUST NOT be rewritten.

### 2.2 Candidate result shape

`shared_carrier_court()` executes SQL and passes every result through `stage_a_norm(rows)`, producing a deterministically sorted list of row arrays.

It then compares that list directly against the mixed-shape B1 oracle using `==`.

Therefore a correct candidate cannot satisfy the real comparison even when the underlying answer is identical.

### 2.3 Q01 semantic query divergence hidden by synthetic data

`make_oracle()` defines `Q01_HOSTILE_STATE_COUNTS` only over the required hostile variable set.

The shared SQL map currently groups all selected variables because Q01 has no hostile-variable predicate.

The synthetic Stage-A fixture contains only hostile variables, so the defect was invisible there. The real B1 fixture contains 48 selected variables, including 16 filler variables; therefore the real oracle and SQL answer diverge even after shape normalization.

Binding correction: Q01 MUST be restricted to the exact source-specific required hostile variables frozen in `HOSTILE`.

No variable semantics are changed by this correction.

### 2.4 Q06 comparison law divergence

Section 9 of `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md` requires exact equality except weighted floating sums, which use absolute/relative tolerance `1e-9` after finite-value validation.

The current shared validator uses plain equality for Q06.

Binding correction: Q06 MUST use the frozen finite-value absolute/relative `1e-9` tolerance; every other query remains exact after canonical normalization.

## 3. Sole permitted harness correction

Only `SR04_CARRIER_BAKEOFF.py` may change.

Implement exactly these comparison-path repairs:

1. one deterministic, non-mutating `canonicalize_frozen_oracle(...)` helper that converts the existing frozen B1 oracle into the exact canonical row-array shape consumed by shared candidate comparison;
2. one shared `oracle_answer_equal(query_id, observed, expected)` helper used by both the cheap proof and REAL B2 validation;
3. Q01 shared SQL restriction to the exact required hostile source-variable sets;
4. Q06 finite-value absolute/relative tolerance `1e-9` in `oracle_answer_equal`;
5. no change to the B1 checkpoint, source decode, fixture relations, Q00/Q02-Q15 query semantics, candidate storage implementations, replay digests, timing loops, indexes, budgets, or selection law.

### 3.1 Canonicalization schemas

Canonicalize the frozen oracle without guessing:

- Q00 -> `[source_id,var_name,count]` rows;
- Q01 -> `[source_id,var_name,physical_state,count]` rows;
- Q02/Q09/Q13 -> `[raw_value_key,count]` rows;
- Q03/Q08/Q10 -> `[key1,key2,count]` rows;
- Q04 -> `[key1,key2,key3,key4,key5,count]` rows;
- Q11 -> `[benchmark_coord_a,benchmark_branch_id,raw_value_key,count]` rows;
- Q12 -> `[var_name,physical_state,count]` rows;
- Q15 -> `[benchmark_branch_id,raw_value_key,count]` rows;
- Q05/Q06 -> one scalar row `[[value]]`;
- Q07 -> event records projected in exact `REL_COLS["events"]` order;
- Q14 -> `[label,count]` rows.

For multi-column dictionary keys serialized by B1, parse only the frozen Python tuple-literal representation using a safe literal parser. Reject malformed keys, unexpected arity, duplicate canonical rows, unexpected query IDs, or unsupported shapes.

Then apply the same deterministic row normalization/sorting used for candidate results.

## 4. Cheap proof required before another REAL B2

Add an explicit proof mode, recommended CLI:

`--real-oracle-canonicalization-proof`

It MUST NOT run B1, B2, raw-source decode, persistent carrier materialization, or PostgreSQL.

It may read the accepted checkpoint only.

Proof path:

`checkpoint_read -> canonicalize frozen QUERY_ORACLE -> register accepted checkpoint relations in one in-memory DuckDB connection -> execute the exact shared Q00-Q15 SQL map once per query -> normalize through the exact shared candidate normalization -> compare through the exact shared oracle_answer_equal -> STOP`

The proof is not a carrier benchmark. No candidate timing or selection evidence may be emitted.

Required assertions:

- `checkpoint_identity_pass = true`
- `checkpoint_mutated = false`
- `raw_source_decode = false`
- `carrier_court_executed = false`
- `persistent_candidate_materialized = false`
- `postgres_started = false`
- `DATABASE_URL_unused = true`
- `frozen_oracle_original_unchanged = true`
- `canonical_query_count = 16`
- `shared_query_map_used = true`
- `shared_candidate_normalizer_used = true`
- `shared_oracle_comparator_used = true`
- `Q00_pass` through `Q15_pass` all `true`
- `all_Q00_Q15_pass = true`
- Q01 filler variables excluded from observed SQL result;
- Q01 canonical observed result exactly equals the canonicalized frozen B1 Q01 oracle;
- Q06 observed and expected values are finite;
- Q06 exact frozen tolerance path passes;
- an artificial Q06 perturbation within `1e-9` tolerance is accepted;
- an artificial Q06 perturbation beyond tolerance is rejected;
- wrong-oracle negative detection remains true under the canonical comparison path.

Required token:

`PRE553_SR04_REAL_ORACLE_CANONICALIZATION_PROOF_PASS`

## 5. Preservation law

The following remain immutable:

- `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`;
- all six accepted checkpoint file hashes/sizes;
- frozen relation digests;
- frozen B1 oracle bytes and oracle digest;
- accepted PostgreSQL UTF-8 correction;
- accepted shape-agnostic wrong-oracle corruption helper;
- candidate set;
- candidate storage/layout law;
- Q00/Q02-Q15 SQL semantics;
- Q00-Q15 names;
- replay law;
- performance law;
- selection law.

This correction makes the shared validator compare information-equivalent representations under the already-frozen query contract. It does not create new empirical answers.

## 6. Publication / stop law

After the cheap proof passes:

1. syntax/static check;
2. verify only `SR04_CARRIER_BAKEOFF.py` changed;
3. commit only that file;
4. commit message: `Fix SR04 real-oracle canonical comparison`;
5. push the control branch;
6. return proof receipt, new harness commit, new harness SHA-256 and final git status to HQ;
7. STOP.

REAL B2 remains unauthorized until HQ separately inspects and accepts this correction/proof.
