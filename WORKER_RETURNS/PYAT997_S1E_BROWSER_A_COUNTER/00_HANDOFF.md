# PYAT #997 — Agent A finite counter to Agent B (R4)

**Disposition: IN-SCOPE COUNTER-REPAIR COMMITTED, SOURCEFREE CODE-CANDIDATE; NOT P0/P1 ACCEPTED; DISTINCT NONAUTHOR G5 NOT_RUN.** This is A's finite authorized counter after B's single hostile examination, not another campaign or an authorized merge.

## 1. Exact source and writer custody

- Controlling issue: [#997](https://github.com/maidiu/rawlsing/issues/997), with phased **P0 source→persisted 13-family bodies→cold first-consumer proof FIRST**, then P1 S1-C/issued/native receipt-fate join, original [#918](https://github.com/maidiu/rawlsing/issues/918), R3C/R3S [#909](https://github.com/maidiu/rawlsing/issues/909), MCR-lite. No 35 original sources or live science rights granted.
- Adversary B source/return: [PR #1018](https://github.com/maidiu/rawlsing/pull/1018), exact parent `e05a0993c5e93bce47c48d52887a4d5f39e1c11d`; B code/test `448a3b3b7aad0f134c8c4d0c27ef85277c905bdd`. B itself descends from A's `045d0f91b419b5f13f914957f3d622ed9ec12934`.
- A counter branch: `agent/pyat997-s1e-agent-a-counter-b-descendant-20261113-r4`, created at B's exact frozen HEAD. Its code+test cut: `be8b30552d9d273b585da17c52dafe5c4c25478c`; exact-AST stdlib probe included in `0123981621b2b37c8ee7c7a94f80e8d7c8a46779`. Final handoff HEAD should be read from the branch/PR after this document's commit.
- Exact B→A compare: **3 changed paths only** before this handoff: `rawlsing_next/pre553_source_postconsumer_receipts.py` +31 lines, `rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py` +106 lines, and new `WORKER_RETURNS/PYAT997_S1E_BROWSER_A_COUNTER/exact_predicate_probe.py`. This handoff is fourth. No S2-C/D, Q2, native I03/I05, P0 writer, owner-protected paths, original source data, or protected PRE-MAIN edited.
- Protected `integration/pre-main-reconciliation-r1` pinned `6a5c12f04323d74001f9632063ec907f4fc4468e`; no protected ref write, merge, or authority promotion.

## 2. Receiving B's attack — preserve actual victories

**Genuine B victory, retained in full:** A's R3 P1 guard inspected `source_realized`, associated state labels and aggregate source-operation census but did not check Q2's detailed `source_realization` per-key evidence; `emitted=0` and concealed routing would evade the summary check. B introduced `_verify_realized_q2_body_witness` with positive key/body/occurrence checks, and six-field identity conservation of `source_preimage.measure` against operation weight, estimand, design and variance. B's three tests for missing emission, routing flag, and weight preimage remain untouched. Its original R157 source ID versus sealed fixture artifact ID distinction remains respected. B's architecture-preservation choice is correct.

**False accusations:** none established by this counter. B's logical falsifier was correctly described as a P1 input-boundary defect, *not* a demonstrated wrong native fact. Do not retrospectively claim B executed the native pipeline.

**Incomplete B victory:** accepted Q2's `_operation_source_antijoin` additionally checks, for every eligible response-owned key with emitted responses, that **not all `routable_rows` are zero**. It creates `routable_rows` directly from `routing_states['ELIGIBLE_APPLICABLE']`, and derives `routing_unresolved` from presence of `ROUTING_UNKNOWN` / `RULE_UNAVAILABLE`. B's new predicate checked only the favorable `routing_unresolved` field, occurrence, and emission. It did **not** validate actual routing-state contents or the routed-support denominator. A forged positive Q2 detail with emitted response, favorable flags and zero eligible routable rows would pass B's guard despite Q2's original refusal. This is another **P1 source-witness consistency defect**, not evidence that S2-D executed an unsound actual scientific fact.

## 3. R4 engineering delta and tests

**New guard repairs** in `pre553_source_postconsumer_receipts.py`, preserving B's exact prior helper body:

1. Typed witness family is one of the original Q2 supported `RespondentEvent`, `EmpiricalCoordinateFact`, `WeightMeasureFact` families.
2. Validate routing-state census mapping as nonnegative integer counts. For response witnesses, require `routable_rows == routing_states.get('ELIGIBLE_APPLICABLE',0)`; require `routing_unresolved` to equal the original Q2 unresolved-state membership test. Refusal `Q2_REALIZATION_ROUTING_CENSUS_DRIFT`.
3. For response-emitted witnesses, group `routable_rows` **by key**, refuse if every emitted response slot for any one key has zero eligible routed support. Refusal `Q2_REALIZATION_ZERO_ROUTABLE_DENOMINATOR`. Does NOT require every slot to be routed: Q2 permits zero slot beside a positive sibling.
4. For non-response witnesses, refuse a forged routing census or non-null `routable_rows`; B's body, occurrence, HELD/UNKNOWN and measure checks remain unchanged.

**Repository tests authored:** +3 parametrized negative cases using real generated Q2 handoff/cold admission fixture before modifying one detailed witness: zero routed support across all emitted slots of a key, concealed `ROUTING_UNKNOWN` within the census, and `routable_rows` vs routing-state eligible count drift. +1 synthetically constructed positive/negative pair proves a zero-support slot next to a positive sibling remains allowed while all-zero route refuses. No xfail/skip or accepted test edits.

**Executed, narrow evidence:** a separate pure-stdlib predicate harness in this assistant's Python container performed **8 passed in 0.05s**: five B-admitted/A-refused synthetic detail defects (including nonresponse forged routing and invalid family) and three positive/pending/mixed-slot preservation checks. The harness faithfully mirrors the B/A helper predicates but does not import the private repository; therefore it is **NOT** a repository pytest red→green, source-authenticated run, nor native proof. A second reusable, dependency-free `exact_predicate_probe.py` is committed. It extracts the **actual** frozen B and current A helper ASTs from a qualified Git checkout with `git show` and compiles/executes them in isolation; it has **not** been run against that checkout here. Run:

```bash
python WORKER_RETURNS/PYAT997_S1E_BROWSER_A_COUNTER/exact_predicate_probe.py
```

It is deliberately not a fake native acceptance test. It uses synthetic Q2 witness rows and returns exact source hashes and B-admit/A-refuse observations.

## 4. Current complete mission obligations — not inferred passed

| Proof | Status |
| --- | --- |
| G1 original35/operation/source no-drop ledger at scoped sourcefree grade | Previous inherited code, not reexecuted |
| P0 one SAV/DTA source decode/projection + all exact 13 bodies→unchanged S2-C | Candidate only; **NOT_RUN** at B/A descendant |
| P0 direct I02 physical/logical equality→cold native I03/I05/Batch→changed fact→restore | **NOT_RUN** |
| P0 actual resource counters, RSS, temp/retained disk, throughput | **NOT_MEASURED**; #1006 owns separate physical performance profiling |
| P1 original S1-C pending/held/eligible→real issued job/consumer receipts and correct fates | Candidate guard strengthened; native **NOT_RUN** |
| P1 native I03/I05/Batch (including completed/partial/absent resume) and independent adversarial replay | **NOT_RUN** |
| Independent B against this A descendant / distinct nonauthor G5 receiving | **NOT_RUN** — B's prior review is NOT G5 of R4 |
| Original35 source/issuer/science/production authority | **HELD_EXTERNAL** |
| Protected branch write/merge/S3 | **NONE** |

The remote hosted workflows for earlier A cut failed before steps, not Python. In this session private repo cannot be cloned directly into the Python execution container and PyArrow/DuckDB/pyreadstat are absent; the dedicated exact-source script is available for an authorized qualified checkout but no native result is claimed.

## 5. New defects and remaining strongest hostile surfaces

- **Independence limit:** R4 strengthens internal Q2 source-witness consistency only. Coherent malicious rewrites of all witness rows, their original key roster/semantics, and aggregate census could still be self-consistent. No independently held, separately signed per-operation census is exposed to this P1 sidecar. A guard is not a new issuer; challenge actual independently held source/I02 and consumer identity, not just mutated Python dicts.
- **Native reality remains the primary missing work:** challenge Q2 original source→journal→S2-C second I02 physical SHA, 13 family typed absences, repeated occurrence, private scratch cleanup, cold first consumer and actual Batch receipt parity. Force one valid changed source cell to change real I03/I05/Batch/possibly F4 fact, then exact restore.
- **P1 authority and completeness:** challenge missing eligible issued receipt, multi-unit discovery, nonterminal completed-then-revoked CURRENT, mixed-source Batch results, duplicate postconsumer candidates and forged/missing HELD/UNKNOWN axes. A favorable scoped receipt does not prove original35 scientific support.
- **R4 false-refusal challenge:** attempt a legitimate Q2 `ELIGIBLE_REALIZED` with multiple response slots, one `routable_rows=0`, another positive. R4 explicitly **accepts** that case; a genuine recorded source counterexample is still worth examining.
- **No further broad A/B campaigns:** proceed to qualified runner, exact in-scope fixes if executable failure occurs, then distinct G5. Do not rewrite accepted S2-C/D or wait for all 35 real sources before P0.

**Current verdict:** `REVISE_EXACT_DEFECT__A_FINITE_COUNTER_COMMITTED__NATIVE_P0_P1_AND_DISTINCT_G5_PENDING__SOURCEFREE_ONLY__PROTECTED_UNCHANGED`.
