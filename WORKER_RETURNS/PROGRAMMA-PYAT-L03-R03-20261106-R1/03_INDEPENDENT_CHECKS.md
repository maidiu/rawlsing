# 03 — Independent discriminating checks and results

The checks in this file were written by the R03 reviewer, not by the
implementation author. They use only accepted fixtures, the existing sealed C11
repository, and the actual `CarrierNeutralResearchExecutor.execute_i03` /
issued-workload first consumers. No production source was modified.

Reproducer scripts are in `reproducers/`; machine-readable receipts are in
`evidence/`.

## 1. Row-level oracle (not the author’s expected values)

`reviewer_checks.py` builds the N=200 synthetic sealed source with
`bench_common.build_main_source(200)`, then derives the expected result directly
from the fixture rows:

- risk set `R` = all respondent ids; `S` = even-index respondent ids;
- condition truth:
  - “all” operations: every respondent;
  - `cond_X1_target_Y`: `X == 1`;
  - `cond_Y1_target_X`: `Y == 1`;
  - `xor_condition_target_Z`: `X != Y`;
  - `minority_branch_target_K`: exact member refs read from the predicate’s
    `DERIVED_BRANCH_COHORT` leaf and mapped back to row ids;
- the target cell is the exact response tuple for 1/2/3/4 targets;
- raw cells/support and weighted cells/denominator are computed from the fixture
  weights (`1 + (i mod 4)`), not from the evaluator.

For each of the 13 operations it compares baseline (no scope) and grouped
candidate to the oracle on: typed state, raw numerator/denominator/resolved
support, risk/denominator member sets, every complete cell’s raw and weighted
counts and cell state, weighted denominator/numerator, measure kind, and risk-set
type. It also requires baseline and candidate full `EmpiricalFact.as_dict()`,
fact refs, and replay refs to be identical.

Result: **PASS for all 13 operations in both baseline and grouped modes.**
Cold grouped scope: `core_builds=11`, `core_hits=2`, `fallbacks=0`.

The full-fact comparison also covers `_UsedObjectAccumulator` /
`_UsedAuthorityAccumulator` output order and deduplication: provenance refs,
authority snapshot refs, and dependency refs are canonical and identical to the
unshared path for every operation.

## 2. Same-world index cut and exact restore

Using the same candidate executor and the same live scope:

1. Removed the repository’s `_i03_release_indices` entry and its attestation for
   the release/universe key. The next `execute_i03` call rebuilt the index from
   the sealed release, producing a new index object.
2. Re-executed all 13 operations. The scope built 11 new cores for the new index
   object and did not reuse any prior core across the rebuild. All facts, fact
   refs, and replay refs still matched the baseline/oracle.
3. Restored the exact original index object and its original attestation.
   Re-execution reused only the original 11 cores (13 hits including the two
   compatible siblings) and produced exact baseline facts again.

Receipt after cut: `core_builds=22`, `core_hits=4`, `fallbacks=0` (two hits are
the intra-mix `all_K` sibling hits on the rebuilt index). Receipt after restore:
`core_builds=22`, `core_hits=17`. No stale group crossed the rebuild.

## 3. Poisoned core refusal

After a successful grouped run, the reviewer replaced the cached core under its
existing key with five independently forged variants while leaving the stored
fingerprint stale:

1. forged `raw_cells` count (+999 in one cell);
2. forged `fact_state` (`ZERO_SUPPORT`);
3. forged `cell_by_respondent` value (`__R03_FORGED_CELL__`);
4. truncated `used_objects`;
5. truncated `used_authority_refs`.

For each variant, the next operation detected the fingerprint mismatch, evicted
the entry, fell back to the unshared path, and published the exact baseline fact
(fact ref and full `as_dict()`), never the forged value. `fingerprint_failures`
increased for every variant (5 total). Restoring the true core resumed exact
grouped execution.

Scope of this result: it is an accidental/stale-corruption check. It does not
claim to defeat an adversary who can both mutate the cache and recompute the
fingerprint; that is outside the accepted same-UID threat scope.

## 4. Refusal and negative parity

- **Weight-basis refusal.** A query identical to `all_K_weighted` except
  `weight_basis_id = W2` (no W2 weight facts exist) was executed with and without
  a scope. Both produced the same `UNAVAILABLE` /
  `MEASURE_UNAVAILABLE` fact and fact ref. The grouped path fell back at least
  once; it did not reuse the W core as a SUPPORTED result.
- **Authority DENY.** The focused grouping suite’s nonpositive
  `PREDICATE_GRAMMAR` case produced the same
  `UNAVAILABLE` / `MISSING_REQUIRED_AUTHORITY` fact with and without the scope;
  grouping was not reached for the denied operation.
- **Zero support.** An empty exact branch predicate produced the same
  `ZERO_SUPPORT` fact in both paths.
- **Special typed states.** The accepted `special_state_fixture()` with
  `MISSING`, `DK`, `REFUSAL`, `IAP`, `NOT_ASKED`, and a substantive response
  produced identical baseline/candidate facts and matched the accepted fixture
  fact’s cell projection, denominator, and `SUPPORTED` state. The event/routing
  state vocabularies remained the accepted tuples. `NOT_ADMINISTERED` is still
  absent from the C11/I03 typed state contract and was not invented.
- **Unsupported topology.** The focused suite’s `LOSSY_UNKNOWN_TOPOLOGY` case
  produced `UNRESOLVED` / `UNSUPPORTED_RESPONSE_TOPOLOGY` in both paths and did
  not build a group (`core_builds=0`).

## 5. P41 / issued-path actual use and parity

`p41_scope_probe.py` wraps only the class used by
`execute_issued_workload` to capture the owned scope receipts; it does not alter
the implementation. The P41 same-source path created **three** owned scopes
(partial run, resumed run, full run), each with builds and two with hits. In the
recorded run: 129 core builds, 368 hits, 165 `capacity_fallbacks`, 0 generic
fallbacks. The scopes closed with `open_groups=0`.

`p41_parity_probe.py` then ran the same P41 path twice — once with the normal
grouped class and once with the class forced to a closed scope (unshared
baseline) — using the same fixed source path and P41 runtime. Result:

- `hashes_equal = true` (trace, view hash, refusal codes),
- `view_hash_equal = true`,
- `view_state_equal = true`,
- `consumer_values_equal = true`.

This is actual first-consumer evidence for issued Batch/I05/P41, not a
private-kernel label.

## 6. W03/W04 physical probe

`w03_w04_probe.json` records:

- With pyarrow installed and `RAWLSING_C11_ACCELERATOR_DIR` unset, the derived
  release public-object view is `_CompactPublicObjects` (in-memory compact Arrow
  lane); no persistent files were created.
- With the caller-configured env root set, one
  `c11-events-a.parquet` slot was written (19,333 bytes for the small fixture) and
  a second call reused the same slot. The 160 selector rows are the exact event
  selectors.
- The existing 8-test compact-view suite passed in the focused 100-test run,
  including delete/corrupt/stale/revoked behavior from the accepted Phase-1
  evidence.

This confirms the selected physical capability exists. It does not establish
economical cold construction or lower peak memory on the real compact
source-backed consumer, which remains open (see `04_LIMITATIONS_AND_REPAIR.md`).
