# PYAT C1-03A — INDEPENDENT-REVIEW REPAIR — R1

Status: `PASS_C1_03A_REVIEW_REPAIR__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq150-c1-03a-review-repair-r1`
Base: `a3c07426b0ad547287cc729b23cd8428c9fc0018` (the C1-03A implementation)
Review: `agent/reviewer-pyat-hq149-c1-03a-r1 @ 6bc1cb8e` — `CHANGES_REQUIRED`

## What this repair does

Three blockers, nothing else. The valid 157-test work underneath is preserved;
C1-02 stays closed.

I reproduced each reviewer counterexample against my own owner **before**
changing anything. All three reproduced exactly:

- a `ProducerStateEvidence` with `producer_state='SUPPORTED'` and a
  caller-chosen `retained_state='VALID_EMPTY'` was accepted;
- `assert_route_not_laundered` accepted a caller-supplied
  `required_route_class='DIRECT_EMPIRICAL'` for the same failed structural-use
  situation and did not raise;
- `build_state_route_result` accepted a positive recursive-handoff ref with
  `coverage_record_ref=None`.

## 1. STATE-PROJECTION — retained state is now owner-derived

`ProducerStateEvidence` requires a module-private token. A caller label now
raises `OwnerProjectionError` citing the blocker id.

Retained state is computed by `OwnerStateProjection` factories that read real
owner objects:

| Factory | Law |
|---|---|
| `from_empirical_fact` | `classify_empirical_cells(fact.typed_state, complete_cell_semantic_projection)` |
| `from_discovery_receipt` | `classify_discovery_receipt_state(typed_state, coverage_state)` with a receipt/coverage disagreement guard |
| `from_adaptive_result` | `classify_adaptive_coverage(...)` plus the owner's own unvisited refs and `global_negative_claim` fact |
| `from_owner_refusal` | the owner declined; the exception type is recorded |

Two subtleties I had to get right:

- **A SUPPORTED fact must carry its cell projection.** Without it an observed
  zero cannot be derived, so a plain positive would be indistinguishable from an
  observed zero. The projection fails closed instead of defaulting to SUPPORTED.
  Nonpositive failure states legitimately carry no cells, and for those the fact
  state alone is decisive.
- **An observed-zero cell on a non-supported fact is refused.**

The AT16 54/6 witness is corrected as instructed: the real cells are
`{support: 54, oppose: 6}` with denominator 60, so the derived state is
`SUPPORTED`, and the court now asserts it is explicitly *not* `OBSERVED_ZERO`.

## 2. ROUTE-DERIVATION — the obligation comes from the owner

`assert_route_not_laundered` now takes `(route_class, obligation)`. The
caller-supplied `required_route_class` parameter no longer exists.

`RouteObligation.from_structural_admission` binds the receipt, rule hash,
admission authority, empirical-fact ref, receipt-declared target use, decision and
reason. Its `obligation_hash` is a pure function of those owner identities, and
it is bound into the envelope identity.

A genuine positive route is now proven — the reviewer's positive-case gap:

```
ADMITTED / EXACT_NAMED_RULE_ALL_GATES_PASS
target_use = STRUCTURAL_MEDIATION_INPUT, rule hash bound
```

One owner behaviour worth recording: with `rule=None` the admission owner reports
`target_use = UNRESOLVED_STRUCTURAL_USE`, not the requested use, because no rule
passed. The obligation records the receipt-declared use verbatim rather than
assuming the requested one. The negative and positive cases are asserted
separately.

Same evidence cannot become direct by relabelling: one receipt is evaluated once,
the LEARNED route is accepted and the DIRECT label is refused for that same
receipt. A competent direct empirical product still routes `DIRECT_EMPIRICAL`
with `authority_refs == ()` and no obligation.

## 3. HANDOFF-COVERAGE — positive selection needs custody

`RecursiveCoverageCustody.from_handoff` requires an exact `evaluated_frontier_ref`
and cross-checks it against the handoff's own retained scope context.

`build_state_route_result` refuses:
- a recursive-handoff producer with no custody,
- custody naming a handoff absent from the producer refs,
- a declared `coverage_record_ref` that disagrees with the custody record,
- custody used to represent UNVISITED territory.

The custody hash is in the envelope identity, so it cannot be dropped silently.
The exact hostile — positive handoff + positive retained state + missing coverage
record — is added and proven.

## Test obligations

| Court | Tests |
|---|---|
| corrected C1-03A | 38 (20 accepted + 18 new blocker courts) |
| accepted C1-02 six-file | 109 |
| adaptive discovery | 11 |
| structural admission | 17 |
| **total** | **175 passed, 0 failed** |

157 + 18 = 175. All 20 original C1-03A courts remain present — rewritten to
derive state from owners, none deleted. **Only these ten files were executed; no
broader regression sweep is claimed.**

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-REVIEW-REPAIR-R1/**`

No existing owner modified. C1-02 untouched.

## Non-claims

No new semantic or model authority. No architecture warrant. No owner gap. No raw
source access. No C4, no C1-03 join, no C1-R, no V3 actor/person work. Not merged,
not self-adopted.

## Terminal

`C1_03A_REVIEW_REPAIR_RETURNED__HQ_ADJUDICATION_REQUIRED`
