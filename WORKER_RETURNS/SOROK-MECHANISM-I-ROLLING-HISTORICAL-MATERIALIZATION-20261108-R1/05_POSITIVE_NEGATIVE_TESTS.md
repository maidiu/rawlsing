# Mechanism I acceptance evidence

Implementation `529485bdfc8a2651013124da11dbaa273cf2f16d`, exact tree
`217626de33a1113bdbe4f0a4f3f7cf305199eb4e`. The sourcefree cut uses the
existing P2/P3/P4 and S46 owners. A mock result establishes the engineering
path at the tested scope. Live model qualification is tracked separately.

```sh
python -m pytest -q rawlsing_next/tests/test_sorok_history_{owner,admission,provider,wake}.py
```

Evidence prefixes in the tables refer to `rawlsing_next/tests/test_sorok_history_*.py`.
Exact older provider and owner receipts are in [02](02_MODEL_PROVIDER_AND_JOB_RECEIPTS.md)
and [03](03_HISTORICAL_ADMISSION_AND_INDEX_EVIDENCE.md). The observed scope
column distinguishes a tested case from the wider commission requirement.

| Case | Status at this cut | Observed scope or remaining proof |
|---|---|---|
| P01 | Scoped pass | Owner checkpoint test binds actual movement and rejects a fabricated event; P4 automatically binds a tool affordance and a confirmed repair output. Arbitrary ingress remains open. |
| P02 | Scoped pass | Owner checkpoint rollback, duplicate admission, cold reopen and repair recovery cases. |
| P03 | Not run live | Wake tests cover real HTTP transport to a controlled endpoint. No authorized model endpoint was configured. |
| P04 | Scoped pass | Owner H0 commit and cold inspection with actor-state preservation evidence. |
| P05 | Partial | Existing repair role and event are bound. H1 evaluator accepts a controlled episode. New H1 ownership and provenance events are not committed. |
| P06 | Partial | Actual repair participant identity is qualified. Actor-state linkage and access remain held. |
| P07 | Scoped pass | Owner checkpoint test commits a compatible physical group and rejects a contradictory one. |
| P08 | Partial | Owner tests rebuild and query actor-to-repair-output links. Practice and actor-claim indexes remain open. |
| P09 | Scoped pass | Cold P4 reads exact committed physical ID. Unperceived repair target and its fact are withheld. |
| P10 | Partial | Explicit inspection of a missing named predicate queues a bounded job. Automatically discovered linked history remains open. |
| P11 | Held | S46 independently produces a target. The existing activity ABI does not consume its newly admitted depth. |
| P12 | Partial | Owner test binds two particulars to the exact same movement event and rebuilds their reverse index. Broader cross-object history joins remain open. |
| P13 | Partial | Direct and nested forks cold-reopen with isolated child targets and no inherited jobs. Shared pre-contact historical choices remain open. |
| P14 | Scoped pass | Cold inspection and stored candidate recovery reuse the exact admitted fact without a provider recall. |
| P15 | Measured scope | Same-fixture cold and warm results in [06](06_PERFORMANCE_AND_RESOURCE_COST.md). No live model latency or production SLO. |
| P16 | Partial | Actual resource and repair artifact ingress. Controlled collection and artifact surface assertions. Institution-linked runtime case remains open. |

| Case | Status at this cut | Observed scope or remaining proof |
|---|---|---|
| D01 | Not run | Shared pre-contact admission and inspection-order comparison remain open. |
| D02 | Partial | Inspection promotes or narrows an objective property request. Wording and shared-history differential remains open. |
| D03 | Partial | Stale world and missing exact parent refusals pass. Paired unrelated-fact survival through parent change remains open. |
| D04 | Partial | H3 undercall and arbitrary effects held in the evaluator. End-to-end irrelevant-edge differential remains open. |
| D05 | Not run | Book appearance and reading or ownership alternatives remain open. |
| D06 | Not run | Prestige commodity and actor-private relations remain open. |
| D07 | Scoped pass | Actual P4 inspection returns pending status while the physical job is pending. |
| D08 | Partial | An objective repair fact remains inaccessible to the user. Actor testimony and user inference contrast remains open. |

| Case | Status at this cut | Observed scope or remaining proof |
|---|---|---|
| N01 | Evaluator pass | H3 and undercalled H3 are held. No V3 write path. |
| N02 | Evaluator pass | H2 without qualified slack held. No CAN/ADP writes authorized. |
| N03 | Evaluator pass | Late parent, custody conflict and closed-effect rejection. Full cross-source travel court remains open. |
| N04 | Scoped pass | Contradictory visible condition rejects at evaluator and owner. |
| N05 | Partial | Fabricated event refused. Explicit user-speculation and actor-testimony differential remains open. |
| N06 | Scoped pass | Actual movement changes readset, stale result refused, old token fenced, bounded retry. |
| N07 | Partial | Same-branch concurrent owner leases and idempotent admission. Shared-root cross-branch singleflight remains open. |
| N08 | Partial | Checkpoint rollback, expired attempt, saved candidate replay, repair enqueue recovery, reverse-index rebuild. Complete kill-point matrix remains open. |
| N09 | Partial | Real direct and nested fork isolation and unperceived fact withheld. Cross-user rights proof remains open. |
| N10 | Scoped pass | Missing dependency rejection and cold inspection refusal when the exact event is detached. |
| N11 | Evaluator pass | Unknown versus known negative tested. P4 pending status remains distinct. |
| N12 | Partial | Physical inspection withheld for unperceived repair. Objective L3 production and actor testimony remain open. |
| N13 | Partial | Instruction-like document text remains in data, and authority stays in the owner. No live adversarial model run. |
| N14 | Scoped pass | Unconfigured runtime reports `LIVE_PROVIDER_NOT_RUN` and the mock HTTP result is graded separately. |
| N15 | Open | Existing P6 fixed-house regression not rerun at this cut. |

Observed local exit code 0, using the existing Sorok test environment.

```text
.............................................                            [100%]
45 passed in 77.86s (0:01:17)
```
