# FIABC-T3 — Oracle Freeze / Process Envelope Transposition

Branch: `agent/rabochii-premain-fiabc-t3-oracle-process-envelope-r1`

Base: `agent/rabochii-premain-fiabc-t2-candidate-c-six-cell-binding-r1`

Exact T2 tip used as branch base:

`eb190a1f2950baf8f0ae52e9832e9d58d0d3d9cc`

Implementation code-seal tip before final return refresh:

`69e8e8cf4128bdd45977688094e9bf97bb4a5aed`

## Disposition

PASS — the independent oracle freeze boundary and fresh source×candidate process envelope are transposed onto the current FIABC-T2 six-cell execution line.

No real source materialization was performed. No measured P2X was run.

## Causal execution law

The live execution contract now enforces:

`SOURCE IDENTITY FREEZE`
→ `AUTHORITY/WORKLOAD FREEZE`
→ `INDEPENDENT ORACLE MATERIALIZE/FREEZE`
→ `CANDIDATE PROCESS START`
→ `C11`
→ `I03`
→ `I05`
→ `LIFECYCLE`
→ `TERMINAL VERIFICATION`.

The current manifest retains its historical stage labels. `S03_PARITY_ORACLE_GATE` is no longer allowed to create expected truth or run candidate self-replay. It is now only a binding check that the independent source-local oracle was already frozen upstream. The complete candidate-vs-oracle comparison remains downstream of complete I03/I05 observation and therefore cannot be replaced by the old S03 self-replay bit.

## Oracle freeze transposition

The accepted Wave-3 I05 module was transposed:

- `rawlsing_next/pre553_independent_parity_oracle.py`

The current T2 backend no longer creates a candidate-local pseudo-oracle in S03 and no longer calls candidate I03 twice to infer parity.

Before any candidate handler executes, the backend binds the source-local oracle identity from the already-frozen candidate-neutral upstream receipt. The receipt must prove:

- no candidate output existed at freeze;
- no candidate-owned root was consulted;
- no candidate-owned state was reused;
- source identity freeze preceded authority/workload freeze;
- authority/workload freeze preceded oracle materialization/freeze;
- the result is read-only frozen.

If those conditions do not hold, the candidate process does not lawfully begin.

## All-source source-root safety

The transposed freeze contract is intentionally not LiTS/WVS-specific.

Each source entry must carry:

- `source_id`;
- `canonical_source_sha256`;
- `source_identity_authority_ref`;
- `derivative_identity` when a derivative is admitted;
- `derivative_to_source_provenance_ref` whenever `derivative_identity` is present.

Derivative identity and derivative-to-source provenance are paired: neither may exist alone.

The process-envelope validator accepts arbitrary source identifiers and binds the exact source named by the active execution manifest. T2 currently exposes LiTS-I and WVS7, but the freeze contract itself can bind any later CLOSED_35 source without creating a source-specific adapter.

## Process-envelope transposition

The accepted I06A execution envelope was transposed:

- `rawlsing_next/ee_p2x_candidate_process_envelope.py`
- `rawlsing_next/ee_p2x_process_isolated_backend.py`

The driver now refuses `--run` / `--resume` unless:

1. `--frozen-upstream-receipt` is present and validates against the current manifest;
2. the selected backend is exactly `rawlsing_next.ee_p2x_process_isolated_backend`.

The long-lived driver imports only the neutral adapter. The actual candidate backend is imported after the candidate-local boundary inside a fresh child process sealed to exactly one `source × candidate` cell.

Cross-cell process reuse, session reuse, candidate-local RSS history, scratch/durable roots, and foreign candidate state fail closed.

Same-cell process retention remains subject to explicit lifecycle transition authorization. T3 does not invent lifecycle permissions owned by the later lifecycle/accounting layer.

## T2 law preserved

T3 does not alter:

- the T2 six-cell capability set;
- Candidate-C identity or source-backed hybrid law;
- LiTS CACC1/CACC2 scope;
- the prohibition on CACC3;
- WVS7 Candidate-C zero-accelerator law;
- canonical LiTS-I or WVS7 source roots;
- the historical/current capability separation;
- T1 stable runtime packaging.

## Qualification boundary

Source-independent hostile tests were added/transposed for:

- candidate-neutral oracle independence;
- generic CLOSED_35-capable source freeze fields;
- derivative-to-source provenance pairing;
- freeze causal ordering;
- direct-backend bypass rejection;
- per-cell process/session/RSS isolation;
- cross-candidate state rejection;
- candidate-neutral upstream capital reuse.

Tests were authored but not executed on this GitHub/browser worker surface. Exact commands are recorded in `04_TEST_COMMANDS.md`.

The branch deliberately does not claim a measured terminal. Actual source-backed oracle materialization remains a local pre-candidate operation, and complete candidate-vs-oracle comparison must consume the complete I03/I05 observation before terminal admission.

## Terminal

`FIABC_T3_ORACLE_FREEZE_AND_PROCESS_ENVELOPE_TRANSPOSED__READY_FOR_NEXT_LAYER`
