# SR04 — REAL-ORACLE CANONICALIZATION PROOF ACCEPTANCE AND B2 RETRY AUTHORITY

Status: `ACCEPTED__REAL_B2_CHECKPOINT_ONLY_RETRY_AUTHORIZED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Accepted B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

Accepted corrected harness implementation: `e249f809f194cb369bf08094ac2cbf4c2d1fcd43`

Accepted corrected harness SHA-256: `e1aa6deaeedf7fb2bbb68c6019e791363e8ad10dcf492087b32a221959e90211`

## 1. Proof adjudication

The bounded real-oracle canonicalization correction is ACCEPTED.

Starting HEAD was `340338a09aa79cd61745c5b7e884d38288fe0a60`.

Correction commit is exactly `e249f809f194cb369bf08094ac2cbf4c2d1fcd43`, message `Fix SR04 real-oracle canonical comparison`.

HQ compare proves the correction is one commit ahead, zero behind, and modifies only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No source, checkpoint, runtime, or governance file was modified by the worker correction.

The proof token is accepted:

`PRE553_SR04_REAL_ORACLE_CANONICALIZATION_PROOF_PASS`

Accepted proof facts include:

- Q00 through Q15 all pass against the immutable B1 checkpoint;
- Q01 observed/frozen canonical row counts are `54 / 54`;
- Q01 filler variables are excluded;
- Q06 observed = `45573.00075805996`;
- Q06 expected = `45573.00075805861`;
- Q06 absolute difference = `1.3533281162381172e-09`;
- Q06 relative difference = `2.969583072711775e-14`;
- Q06 frozen tolerance path and inside/outside perturbation tests pass;
- checkpoint remains unchanged;
- no raw-source decode occurred;
- no carrier court executed;
- no persistent candidate was materialized;
- PostgreSQL was not started;
- DATABASE_URL was unused.

## 2. Static implementation acceptance

HQ static review confirms the real B2 path now:

1. canonicalizes the frozen B1 mixed-shape oracle once through `canonicalize_frozen_oracle(...)`;
2. uses the same `oracle_answer_equal(...)` comparator for each candidate/query pass-fail decision;
3. restricts Q01 to the exact frozen source-specific `HOSTILE` variable sets;
4. applies finite-value `math.isclose(..., rel_tol=1e-9, abs_tol=1e-9)` only to Q06;
5. preserves exact equality for the remaining queries after canonical normalization;
6. preserves the accepted PostgreSQL UTF-8 path, replay digest path, timing path, indexes, budgets, and selection law.

The immutable B1 `QUERY_ORACLE.json` is not rewritten or regenerated.

## 3. Nonblocking harness-hygiene observations

HQ notes two residual code-quality issues that DO NOT affect REAL B2 admissibility:

- `oracle_mismatch_queries` remains a stale diagnostic comparing normalized SQL rows directly to the uncanonicalized oracle. It is not used for pass/fail, candidate disposition, selection, or the final nine-file package and is therefore non-dispositive.
- the new Q07 oracle canonicalizer accepts the real B1 list-of-record-dictionaries form but is stricter than the already-canonical synthetic Stage-A Q07 row-array form. Stage A/A.1/A.2 are already frozen and are not authorized to rerun in this cycle. This is deferred harness hygiene, not a REAL B2 blocker.

Neither issue authorizes another harness modification before the B2 retry.

## 4. REAL B2 retry authority

REAL B2 is now AUTHORIZED exactly once from a new HQ launch HEAD containing only this acceptance/order/ledger bookkeeping after the accepted harness commit.

The retry is checkpoint-only.

Boundary:

`accepted B1 checkpoint -> checkpoint verification -> shared four-candidate court -> canonical oracle comparison -> replay verification -> performance measurements -> provisional selection -> exact nine-file package -> deterministic ZIP -> STOP`

No raw-source decode is authorized.

## 5. Immutable checkpoint identities

Before execution verify exactly:

- `CHECKPOINT_MANIFEST.json` — 4490 bytes — `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0`
- `QUERY_ORACLE.json` — 131552 bytes — `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a`
- `events.arrow` — 104610186 bytes — `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25`
- `respondents.arrow` — 9920410 bytes — `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73`
- `sources.arrow` — 5418 bytes — `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d`
- `variables.arrow` — 33882 bytes — `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b`

Total substantive bytes: `114705938`.

Stop on any mismatch.

## 6. Execution law

Use the accepted harness read-only.

Do not run B1.
Do not pass `--source-root`.
Do not decode WVS7 or LiTS I.
Do not mutate the checkpoint.
Do not use DATABASE_URL.
Do not touch live Rawlsing PostgreSQL.
Do not modify the harness during execution.

Use fresh disposable B2 work/result paths after safely removing only prior failed disposable B2 paths if present and verified not to alias the checkpoint.

Required final token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

No carrier result is accepted until HQ inspects the returned final package and adjudicates G-SR04.
