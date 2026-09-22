# FIABC CANONICAL TERMINAL READINESS REPAIR — R1 RETURN

## Identity

- Exact canonical base SHA: `3206bad6419e02c3aa12fff38e288e4faf13d82d`
- Worker branch: `agent/rabochii-premain-fiabc-terminal-readiness-r1`
- Bounded repair head before return-packet commits: `00cc1c0fbe945cd7bbc6a8187aaf5533c9fb9b38`
- Exact final worker SHA: the authoritative branch-head SHA produced by the commit containing this return file is reported in the worker terminal response. A commit cannot truthfully embed its own resulting SHA in its own content without a cryptographic self-reference; no false pre-commit SHA is asserted here.
- Canonical PRE-MAIN was **not** fast-forwarded by this worker.

## Changed paths

Bounded repair:

1. `rawlsing_next/pre553_independent_parity_oracle.py`
2. `rawlsing_next/fiabc_final_oracle_freeze_producers.py`
3. `WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`
4. `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/02_PRE_CANDIDATE_LOCAL_PREFLIGHT.sh`
5. `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/03_MEASURED_SIX_CELL_RUN.sh`

Return packet:

6. `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/00_RETURN.md`
7. `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/01_CHANGED_FILES.md`
8. `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/02_STATIC_AUDIT.json`
9. `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/03_LOCAL_QUALIFICATION_COMMAND.md`

## LiTS 50/77 authority provenance

The existing candidate-neutral oracle/constitution owner, `rawlsing_next/pre553_independent_parity_oracle.py`, already enforced the LiTS terminal constitution with literal values 50 candidates and 77 query roles. The independent execution manifest `WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json` independently binds `learned_candidates: 50` and `learned_roles: 77`.

This repair mints no authority. It names the already-governing values exactly once at the current owner:

```python
LITS_CANDIDATE_COUNT = 50
LITS_QUERY_ROLE_COUNT = 77
```

All semantically identical LiTS 50/77 checks in that owner now consume those names.

## Exact symbol-ownership repair

`rawlsing_next/fiabc_final_oracle_freeze_producers.py` now imports `LITS_CANDIDATE_COUNT` and `LITS_QUERY_ROLE_COUNT` from `pre553_independent_parity_oracle.py`. Because those imports are module-scope names, the producer now resolves/re-exports the symbols expected by `rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py`.

The producer defines no competing 50/77 constants.

## Exact interpreter-selection repair

Each required shell launch surface now:

1. prefers `python3` when present;
2. otherwise selects `python`;
3. fails immediately if neither executable exists;
4. verifies that the selected interpreter has Python major version 3;
5. stores the selected executable in `PYTHON_BIN` and uses it for every subsequent Python operation.

No bare operational `python ...` invocation remains in the three required scripts.

The source-free qualification script additionally pins the exact repaired oracle and producer Git blobs before allowing those two paths through its existing FIABC reconciliation drift filter. This is required so the canonical qualification does not reject the bounded repair it is meant to qualify.

## Proof of semantic non-change

Static base→worker comparison establishes:

- oracle code, after mechanically substituting the two new names back to literals 50/77 and removing the two definitions, is byte-for-byte equal to the base oracle file;
- producer code, after removing the two new import lines, is byte-for-byte equal to the base producer file;
- all identity-bearing assignment lines in both modules are unchanged;
- LiTS frontier seal, source SHA, learned-product identity, semantic replay identity, projection/release identities, typed-terminal law, candidate ordering, WVS successor Lock2/Lock2 replay/discovery authority, and oracle law were not altered;
- no telemetry metric, candidate implementation, workload constitution, architecture-selection law, or empirical source semantics were changed.

## Static court

All 12 required checks PASS:

1. `LITS_CANDIDATE_COUNT` resolves from the exact authoritative owner.
2. Value is exactly `50`.
3. `LITS_QUERY_ROLE_COUNT` resolves from the exact authoritative owner.
4. Value is exactly `77`.
5. Producer resolves/re-exports both names and defines no competing values.
6. Existing test import now has a valid symbol path.
7. FIABC/WVS/P2/PRE553 semantic identities are unchanged.
8. All three required launch scripts choose and verify Python 3 fail-closed.
9. No bare operational `python` invocation remains in those scripts.
10. Source-free qualification contains no `LITS_PATH`, `WVS_PATH`, `produce-lits`, `standardize-wvs`, `freeze-t3`, `--run`, or `--resume`; its pre-existing import/compile/pytest/static-assertion payload order is preserved after the new interpreter guard.
11. Pre-candidate preflight still uses `--preflight` and contains no candidate `--run` or `--resume`; its pre-existing payload command order is preserved.
12. The measured runner still has one measured-driver `--run`; the frozen manifest remains exactly six cells in order `LITS_I/A`, `LITS_I/B`, `LITS_I/C`, `WVS7/A`, `WVS7/B`, `WVS7/C`, and the driver retains its exact source/candidate order guards and serialized continuation loop.

Machine-readable evidence is in `02_STATIC_AUDIT.json`.

## Local qualification follow-up

The user subsequently ran the required source-free local qualification from exact worker head `97329d51aac6bec495114b5e89e60260c2fcc846` and reported:

```text
154 passed, 9 failed, 28 subtests passed in 9.16s
```

The green terminal was therefore correctly not emitted.

Static browser/GitHub diagnosis found all nine failures to be qualification-test/fixture drift rather than production semantic-law failures:

- one completeness hostile test expected `TC_REQUIRED_METRIC_ABSENT`, but current exact 35-key set validation lawfully fails first with `TC_METRIC_SET_DRIFT`;
- one R1J preflight test required the successor discovery SHA to be textually inlined even though the active backend binds that exact SHA through `WVS_DISCOVERY_AUTHORITY`;
- seven legacy Darwin driver-mechanics fixtures directly supplied synthetic backend receipts without the now-governing exact T3 process envelope required by T4 live accounting.

The bounded follow-up changed only those test/qualification surfaces. It did **not** weaken the production T3/T4 seam: the dedicated T3 process-envelope and T4 live-accounting test suites remain in the source-free qualification command.

See `04_LOCAL_QUALIFICATION_FAILURE_FOLLOWUP.md` for exact diagnosis and repair.

A fresh local source-free qualification rerun is required; this worker did not execute it.

## Second local qualification follow-up

The user reran source-free qualification from `c0fa63e0817bca56566049e86bf192934964868a`. Pytest was fully green:

```text
163 passed, 28 subtests passed in 9.49s
```

Qualification then stopped only in its final static cross-lane assertion because the shell script referenced non-existent `oracle.WVS7_LOCK2_REPLAY`.

The authoritative oracle export is `WVS7_LOCK2_REPLAY_IDENTITY`, and its value exactly equals `WVS7_SUCCESSOR_LOCK2_REPLAY` in live terminal control. The qualification assertion was corrected to that exact symbol. No production Python module or semantic identity changed.

See `05_LOCAL_QUALIFICATION_FINAL_ASSERTION_FOLLOWUP.md`. A fresh local rerun remains required; this Browser/GitHub worker did not execute it.

## Runtime statement

No runtime qualification was executed.

This worker also did **not**:

- open or materialize LiTS/WVS raw survey carriers;
- run Candidate A/B/C;
- generate the LiTS oracle;
- standardize/freeze the WVS oracle;
- run the pre-candidate T3 freeze;
- run measured P2X;
- trigger GitHub Actions.

## Next lawful local command

Run exactly:

```bash
bash WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh
```

Then stop and inspect the source-free qualification result before any source/oracle/candidate work.

## Terminal

`FIABC_CANONICAL_TERMINAL_READINESS_REPAIR_R1__RETURNED__50_77_SYMBOL_BINDING_REPAIRED__PYTHON3_PORTABILITY_REPAIRED__LOCAL_SOURCE_FREE_QUALIFICATION_REQUIRED`
