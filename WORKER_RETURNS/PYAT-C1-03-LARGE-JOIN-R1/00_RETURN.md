# PYAT C1-03 — LARGE THREE-TRUNK INTEGRATION JOIN — R1

Status: `ACCEPTED_OWNER_INTEGRATION_CONFLICT__HQ_ADJUDICATION_REQUIRED`

Branch: `agent/opencode-pyat-hq162-c1-03-large-join-r1`
Commission tip: `9f2f4ee271dac3d2f7673d1d495228db93fe60a5`
Final SHA: `f6456951b68df9d9a2711d8c65ceb3fccbd07612`

**This is not a PASS.** The join itself is sound; one accepted artifact cannot hold
simultaneously with an adopted accepted owner, and that conflict is HQ's to adjudicate.

## Phase 0 — lineage lock: all facts confirmed

Every HQ-stated fact verified exactly. All three accepted tips resolve, both
implementation SHAs are reachable from their accepted tips, both merge bases match
(`bc661188b` for A/R, `5fafb499` for AT17/C1-01), and **all four critical production
blobs match their commissioned hashes byte for byte.** No provenance drift.

## Phase 1 — one integrated tree, zero conflicts

Two ancestry-preserving `--no-ff` merges of the exact accepted tips:

| | merged tip | conflicts |
|---|---|---|
| 1 | AT17/N10E `52e41a41e8bc` | 0 |
| 2 | C1-03R `9ec7eaff2646` | 0 |

All four critical blobs are **byte-identical after integration**. I edited **no**
accepted owner module.

## The one real finding

`rawlsing_next/pre553_analytical_composition.py` is a shared production file modified
on more than one trunk — precisely the Phase 0 census item. It is **not** a semantic
conflict but a stale divergence: AT17's blob `26f3380c` is the C1-01 R8 version from
`e782aba90`, and the A/R trunks received three further C1-02 commits that advanced it
to `604c8d59`. The join correctly resolves to the newer `604c8d59`.

That resolution is what exposes the conflict:

- AT17's `test_p7_frozen_spine_bindings_still_hold_for_the_fixture_law` asserts
  `composed_result_identity_hash == 03610f9d91b2…`
- the adopted owner computes `01c381d3f3c3…`

because C1-02 added **ten identity-preimage fields** the AT17-era owner did not bind
(`discovery_receipt_refs`, `recursive_lineage_refs`, `pairing_ground_truth_materials`,
`pairing_authority_refs`, and six more).

**The owner cannot be reverted.** I proved this in a scratch worktree: with AT17's
older blob, C1-03A's own `test_pre553_analytical_composition_higher_order.py` fails at
**import** — `cannot import name 'DiscoveryConsumptionMismatch'`. The adopted owner is
mandatory for A and R.

**The spine cannot be refreshed here.** It is not a stale test copy. It is
`PYAT_C1_00_R8_CURRENT_AT07_IDENTITY_SPINE@1`, status
`EXECUTED_SOURCE_FREE_CURRENT_IDENTITY`, frozen by an **independent** commission
(`9e2655818`, "Close C1-01 R8 source-free release identity and predicate custody") — not
by the AT17 implementation. Recomputing it from implementation output would make the
assertion tautological and destroy the oracle independence this project enforces in
every commission. I will not self-authorise that re-freeze.

### Smallest required owner question for HQ

> Does the adopted C1-02 analytical-composition identity advancement (the ten added
> identity-preimage fields) **supersede** the R8 frozen AT07 spine's
> `composed_result_identity_hash`?
>
> - **Yes** → commission an explicitly re-frozen spine produced by an **independent
>   oracle run**, not by copying implementation output.
> - **No** → the composition owner must be rolled back, which breaks C1-03A and
>   C1-03R and is therefore not available.

## Phase 8 — union court

Collection reconciles to **exactly 413** across the fourteen accepted suites — no
delta to explain. Plus **22 join courts**.

```
accepted union   413
join courts       22
total collected  435
passed           434
failed             1   <- the frozen-spine conflict
errors/skipped     0
exit status        1
```

The test-file list was generated from disk with an existence assertion. I mistyped
`pre753` for `pre553` twice during this job; the second time produced
`no tests ran in 0.01s`, which reads as a pass unless the output is read. Generating
the list from disk removes that failure mode.

## What the join court proves

All 22 courts pass, using real accepted artifacts only — no fabricated stand-in refs.

**Positive (Phase 3):** AT17 drives query → composition → generated evidence → the
real consumer at `EXACT_SUPPORTED`; A's AT16 positive path still reaches the named
consumer; on the shared 54/6 grain the determinants agree while owner-specific hashes
are correctly *not* required to match. AT17's anti-fabrication property is proven in its
strongest form — **the provider signature and request type have no geometry field at
all**, so precomputed geometry cannot be supplied.

**Negative (Phase 4):** all eight A negative states stay distinct; lifecycle
vocabularies are string-disjoint from analytical negatives; `EXPLICIT_NONCURRENT` and
`NOT_GOVERNED` are never synonyms for `UNRESOLVED`/`VALID_EMPTY`/`INTEGRITY_FAILURE`;
AT17 refusal yields no geometry; A's consumer non-invocation stays explicit.

**Lifecycle (Phase 5–6) — the central proof:** real AT17 and A exact refs registered in
the real R owner classify as **one lawful replacement, one explicit noncurrent, one
identity-stable unaffected CURRENT**, with real changed determinant refs. Zero-release
stays `NO_GOVERNING_RELEASE`, unknown stays `OWNER_UNKNOWN_DEPENDENT`, invalid rollback
is atomic no-commit, and A/U partition the registered dependents exactly.

**Replay (Phase 7):** R checkpoint round-trip reproduces join outcomes exactly; a
separate OS process rebuilds the join lifecycle from checkpoint alone and reproduces the
explicit noncurrent outcome with its exact disposition and reason code; the four replay
grades stay distinct.

## Two things I want to flag honestly

**No single fresh-process bridge exists.** Phase 7's preferred joined proof needs
retained determinants → provider recompute → named consumer → lifecycle restore in one
fresh process. No accepted contract exposes that lawfully. I recorded it as a typed
integration finding instead of fabricating one, and executed both accepted
fresh-process paths in the same tree.

**One hostile I wrote asserted a requirement AT17 does not make.** I expected the
provider to refuse a model rule bound to an ungoverned authority. It does not. Rather
than force the assertion, I checked what actually protects the product: the
composition identity binds the model-rule hash, so a foreign authority yields a
*different* governed identity and cannot masquerade as the real one. The court now
asserts that real property.

## Changed files

Only two new test-terrain files plus the return packet. **Zero accepted owner module
edits. No join production glue** — none was necessary, so none was introduced (a court
asserts its absence).

- `rawlsing_next/tests/c1_03_join_fixture.py`
- `rawlsing_next/tests/test_pre553_c1_03_join.py`
- `WORKER_RETURNS/PYAT-C1-03-LARGE-JOIN-R1/**`

## Non-claims

Not self-adopted. Not merged to control. No C1-R. No raw sources. No C4/C7. No V3
actor/person work. No semantic PRE-MAIN/MAIN change.

## Terminal

`C1_03_LARGE_JOIN_RETURNED__HQ_ADJUDICATION_REQUIRED`
